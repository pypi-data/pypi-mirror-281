"""
Provides a set of functions to work with meteorological data in ``ecsv`` or ``grib(2)`` format.

The molecular absorption cross sections have been retrieved from:
"The HITRAN2020 molecular spectroscopic database",
J. Quant. Spectrosc. Radiat. Transfer 277, 107949 (2022).
[doi:10.1016/j.jqsrt.2021.107949]"

Created by Pere Munar-Adrover (pere.munaradrover@gmail.com)

Further developed and mainted by
* Mykhailo Dalchenko (mykhailo.dalchenko@unige.ch) and
* Georgios Voutsinas (georgios.voutsinas@unige.ch)
"""

import logging
import os
import sys
from bisect import bisect_left

import astropy.units as u
import numpy as np
from astropy.io.registry.base import IORegistryError
from astropy.table import Column, QTable, Table, vstack
from scipy.interpolate import interp1d

from molecularprofiles.utils.constants import (
    DENSITY_SCALE_HEIGHT,
    MOLAR_MASS_OZONE,
    N0_AIR,
    N_A,
    RAYLEIGH_SCATTERING_ALTITUDE_BINS,
    STD_AIR_DENSITY,
    STD_CORSIKA_ALTITUDE_PROFILE,
    STD_GRAVITATIONAL_ACCELERATION,
)
from molecularprofiles.utils.grib_utils import extend_grib_data, get_grib_file_data
from molecularprofiles.utils.humidity import (
    compressibility,
    density_moist_air,
    molar_fraction_water_vapor,
    partial_pressure_water_vapor,
)
from molecularprofiles.utils.rayleigh import Rayleigh

ROOTDIR = os.path.dirname(os.path.abspath(__file__))
log_config_file = f"{ROOTDIR}/utils/mdps_log.conf"
logging.config.fileConfig(fname=log_config_file, disable_existing_loggers=False)
logger = logging.getLogger(__name__)


def _write(table_data, filename, _overwrite=True, format="ascii.ecsv"):
    try:
        table_data.write(filename, overwrite=_overwrite)
    except (ValueError, TypeError, OSError, IORegistryError) as ex:
        template = "An exception of type {0} occurred. Arguments:\n{1!r}"
        message = template.format(type(ex).__name__, ex.args)
        logger.error(message)
        sys.exit(1)


class MolecularProfile:
    """
    Provides a series of functions to analyze meteorological data.

    Methods within this class:

    get_data:                   retrieves the data from the input file.
                                If the input filei is a ``grib`` file,
                                the data is extracted using the grib_utils module.
                                If the input file is an ``ecsv``,
                                ``astropy.Table`` ``read`` method is used.
    write_atmospheric_profile:  writes an ecsv file that contains the atmosphere-related
                                information, required by Corsika simulations.
    create_mdp:                 creates an altitude profile of the
                                molecular number density.
    rayleigh_extinction:        writes a table with the atmospheric absolute optical
                                depth binned in wavelength and altitude into an ecsv file.
    """

    def __init__(
        self,
        data_file,
        stat_columns=(
            "Pressure",
            "Altitude",
            "Density",
            "Temperature",
            "Wind Speed",
            "Wind Direction",
            "Relative humidity",
            "Exponential Density",
        ),
    ):
        """
        Create an instance of MolecularProfile class.

        :param data_file: txt file containing the data (string)
        """
        self.data_file = data_file
        self.data = None
        self.stat_data = None
        self.stat_description = None
        self.stat_columns = stat_columns

    # ==================================================================================
    # Private functions
    # ==================================================================================

    def _interpolate(self, x_param, y_param, new_x_param, kind="cubic"):
        func = interp1d(x_param, y_param, kind=kind, bounds_error=False)
        return func(new_x_param)

    def _compute_mass_density(self, air="moist", co2_concentration=415):
        """
        Compute regular and exponential mass density of air.

        Adds to data the following columns:
        * 'Xw': molar fraction of water vapor (0 if air is dry)
        * 'Compressibility'
        * 'Mass Density'
        * 'Exponential Mass Density'

        Parameters
        ----------
        air : str
            Type of air, can be 'moist' or 'dry'
        co2_concentration : float
            CO2 volume concentration in ppmv
        """
        if air == "moist":
            self.data["Xw"] = molar_fraction_water_vapor(
                self.data["Pressure"],
                self.data["Temperature"],
                self.data["Relative humidity"],
            )
        elif air == "dry":
            self.data["Xw"] = 0.0
        else:
            raise ValueError("Wrong air condition. It must be 'moist' or 'dry'.")

        self.data["Compressibility"] = compressibility(
            self.data["Pressure"], self.data["Temperature"], self.data["Xw"]
        )
        self.data["Mass Density"] = density_moist_air(
            self.data["Pressure"],
            self.data["Temperature"],
            self.data["Compressibility"],
            self.data["Xw"],
            co2_concentration,
        )
        self.data["Exponential Mass Density"] = (
            self.data["Mass Density"] / STD_AIR_DENSITY
        ).decompose() * np.exp(
            (self.data["Altitude"] / DENSITY_SCALE_HEIGHT).decompose()
        )

    # ==================================================================================
    # Main get data function
    # ==================================================================================
    def get_data(self):
        """
        Ingest and pre-process meteorological data.

        Read ECMWF or GDAS data in ecsv or grib(2) format
        and computes statistical description of the data.
        """
        if not os.path.isfile(self.data_file):
            raise FileNotFoundError(f"The file '{self.data_file}' does not exist.")
        file_ext = os.path.splitext(self.data_file)[1]
        if file_ext in (".grib", ".grib2"):
            self.data = get_grib_file_data(self.data_file)
            self.data = extend_grib_data(self.data)
        elif file_ext == ".ecsv":
            self.data = Table.read(self.data_file)
        else:
            raise NotImplementedError(
                "Only grib (1,2) and ecsv formats are supported at the moment. "
                f"Requested format: {file_ext}"
            )
        self.stat_data = self.data[self.stat_columns].group_by("Pressure")
        self.stat_description = {
            "avg": self.stat_data.groups.aggregate(np.mean),
            "std": self.stat_data.groups.aggregate(np.std),
            "mad": self.stat_data.groups.aggregate(
                lambda x: np.mean(np.absolute(x - np.mean(x)))
            ),
            "p2p_max": self.stat_data.groups.aggregate(
                lambda x: np.max(x) - np.mean(x)
            ),
            "p2p_min": self.stat_data.groups.aggregate(
                lambda x: np.mean(x) - np.min(x)
            ),
        }

    # pylint: disable=too-many-arguments
    def _refractive_index(self, P, T, RH, wavelength, CO2):
        """Return Rayleigh.refractive_index."""
        rayleigh = Rayleigh(wavelength, CO2, P, T, RH)
        return rayleigh.refractive_index

    # pylint: enable=too-many-arguments

    def _take_closest(self, my_list, my_number):
        # pylint: disable=line-too-long
        """
        Return closest value to my_number.

        If two numbers are equally close, return the smallest number.
        This function comes from the answer of user:
        https://stackoverflow.com/users/566644/lauritz-v-thaulow
        found in stack overflow post:
        https://stackoverflow.com/questions/12141150/from-list-of-integers-get-number-closest-to-a-given-value/12141511#12141511
        """
        # pylint: enable=line-too-long
        pos = bisect_left(my_list, my_number)
        if pos == 0:
            return my_list[0]
        if pos == len(my_list):
            return my_list[-1]
        before = my_list[pos - 1]
        after = my_list[pos]
        if after - my_number < my_number - before:
            return after
        return before

    def _get_data_altitude_range(self, altitude_profile):
        """
        Calculate the floor and ceiling of the available DAS data.

        Parameters
        ----------
        altitude_profile : Quantity
            Tuple with the altitudes that the atmospheric parameters will be calculated.
            Units of length.

        Returns
        -------
        m_floor, m_ceiling :
            Highest and lowest altitudes, where DAS data is available.
        """
        m_floor = self._take_closest(
            altitude_profile,
            (
                (self.stat_description["avg"]["Altitude"][-1])
                * (self.stat_description["avg"]["Altitude"].unit)
            ).to(altitude_profile.unit),
        )
        m_ceiling = self._take_closest(
            altitude_profile,
            (
                (self.stat_description["avg"]["Altitude"][0])
                * (self.stat_description["avg"]["Altitude"].unit)
            ).to(altitude_profile.unit),
        )
        return m_floor, m_ceiling

    def _create_profile(self, interpolation_centers):
        """Interpolate atmospheric parameters in the requested interpolation centers."""
        parameters_dict = {}
        for col in self.stat_data.colnames:
            parameter = (
                self._interpolate(
                    self.stat_description["avg"]["Altitude"].to(u.km),
                    self.stat_description["avg"][col],
                    interpolation_centers.to(u.km),
                )
                * self.stat_description["avg"][col].unit
            )
            parameters_dict.update({col: parameter})
        return parameters_dict

    def _pick_up_reference_atmosphere(self, m_ceiling, m_floor, reference_atmosphere):
        """
        Merge with the reference atmosphere.

        Pick up the reference atmosphere corresponding to the season and
        the geographical location. It selects all rows above the given ceiling.

        Parameters
        ----------
        m_ceiling
            Astropy quantity expressing the ceiling of the DAS data.
        reference_atmosphere
            ecsv file with the reference atmosphere profile.

        Returns
        -------
        table
            Astropy table with the atmospheric profile above the given ceiling.
        """
        try:
            reference_atmosphere_table = Table.read(reference_atmosphere)
        except (TypeError, ValueError, RuntimeError) as ex:
            template = "An exception of type {0} occurred. Arguments:\n{1!r}"
            message = template.format(type(ex).__name__, ex.args)
            logger.error(message)
            sys.exit(1)
        mask = (
            reference_atmosphere_table["altitude"]
            >= m_ceiling.to(reference_atmosphere_table["altitude"].unit)
        ) | (
            reference_atmosphere_table["altitude"]
            <= m_floor.to(reference_atmosphere_table["altitude"].unit)
        )
        return reference_atmosphere_table[mask]

    def _wavelength_range(self, wavelength_min=200 * u.nm, wavelength_max=1001 * u.nm):
        return (
            np.arange(wavelength_min.to_value(u.nm), wavelength_max.to_value(u.nm), 1)
            * u.nm
        )

    def _interpolate_cross_section(self, molecule_cross_section_file):
        cross_section_table = QTable.read(
            molecule_cross_section_file, format="ascii.ecsv"
        )
        cross_section_table.sort("wavelength")
        wavelength_range = self._wavelength_range()
        cross_section_interpolated = (
            self._interpolate(
                cross_section_table["wavelength"],
                cross_section_table["x_section"],
                wavelength_range,
                kind="linear",
            )
            * u.cm**2
        )
        cross_section_interpolated_table = QTable(
            [wavelength_range, cross_section_interpolated],
            names=("wavelength", "cross section"),
        )
        return cross_section_interpolated_table

    # ==================================================================================
    # printing functions:
    # ==================================================================================

    # pylint: disable=too-many-locals
    def write_atmospheric_profile(
        self,
        outfile,
        co2_concentration,
        reference_atmosphere=None,
        altitude_list=STD_CORSIKA_ALTITUDE_PROFILE,
        write_to_file=True,
    ):
        # pylint: disable=line-too-long
        """
        Write an output file in the style of a CORSIKA atmospheric configuration file.

        File format: tab-separated columns with:
        * altitude (km)
        * density (g/cm^3)
        * thickness (g/cm^2)
        * refractive index -1
        * temperature (K)
        * pressure (hPA)
        * partial water pressure

        Parameters
        ----------
        outfile : string
            Name of the returned file.
        co2_concentration : float
            12MACOBAC value
        reference_atmosphere : path
            The path where the file with the reference atmosphere model is located.
        altitude_list : Quantity
            Tuple with the altitudes that the atmospheric parameters will be calculated.
            Units of length.
        write_to_file : bool
            If true the function writes the Corsika profile into the file `outfile`.

        Notes
        -----
        This function writes the molecular profile to a file, having ecsv format, 
        specified by the parameter `out_file`.

        """
        # pylint: enable=line-too-long

        m_floor, m_ceiling = self._get_data_altitude_range(
            altitude_list.to(self.stat_description["avg"]["Altitude"].unit)
        )
        altitude = altitude_list[
            (altitude_list.to_value() > m_floor.to_value(altitude_list.unit))
            & (altitude_list.to_value() < m_ceiling.to_value(altitude_list.unit))
        ]
        altitude = altitude.to(self.stat_description["avg"]["Altitude"].unit)
        parameters_dict = self._create_profile(altitude)
        temperature = parameters_dict["Temperature"]
        relative_humidity = parameters_dict["Relative humidity"]
        pressure = parameters_dict["Pressure"]
        density = parameters_dict["Density"] / N0_AIR

        thickness = pressure / STD_GRAVITATIONAL_ACCELERATION
        rel_water_vapor_pressure = (
            partial_pressure_water_vapor(temperature, relative_humidity) / pressure
        ).decompose()
        rel_refractive_index = (
            self._refractive_index(
                pressure,
                temperature,
                relative_humidity,
                350.0 * u.nm,
                co2_concentration,
            )
            - 1.0
        )

        tables = []

        for i in np.arange(len(altitude)):
            outdict = {
                "altitude": altitude[i].to(u.km),
                "atmospheric_density": density[i].to(u.g / u.cm**3),
                "atmospheric_thickness": thickness[i].decompose().to(u.g / u.cm**2),
                "refractive_index_m_1": rel_refractive_index[i],
                "temperature": temperature[i],
                "pressure": pressure[i],
                "partial_water_pressure": rel_water_vapor_pressure[i],
            }
            tables.append(outdict)
        # Merge ECMWF profile with upper atmospheric profile
        if reference_atmosphere:
            reference_atmosphere_table = self._pick_up_reference_atmosphere(
                m_ceiling, m_floor, reference_atmosphere
            )
            tables.append(reference_atmosphere_table)
        else:
            logger.warning(
                "Since reference atmosphere was not provided, "
                "the resulting atmospheric model will be constrained "
                "to the extent of the provided meteorological data."
            )
        corsika_input_table = vstack(tables)
        corsika_input_table.sort("altitude")
        _write(corsika_input_table, outfile)

    # pylint: enable=too-many-locals

    def create_mdp(self, mdp_file, write_to_file=True):
        """
        Produce a Molecular (number) Density Profile (MDP).
        
        Parameters
        ----------
        mdp_file : string
            Name of the returned file with the MDP.  
        write_to_file : bool
            If true, the function writes the MDP into the file `mdp_file`.

        Notes
        -----
        This function writes the MDP to a file, having ecsv format, 
        specified by the parameter `mdp_file`.
        """
        
        altitudes = np.arange(0.0, 20000.0, 1000) * u.m
        altitudes = altitudes.to(self.stat_description["avg"]["Altitude"].unit)
        number_density = (
            self._interpolate(
                self.stat_description["avg"]["Altitude"],
                self.stat_description["avg"]["Density"],
                altitudes,
            )
            * self.stat_description["avg"]["Density"].unit
        )
        t = Table([altitudes, number_density], names=["altitude", "number density"])
        _write(t, mdp_file)

    # pylint: disable=too-many-arguments,too-many-locals
    def rayleigh_extinction(
        self,
        rayleigh_extinction_file,
        co2_concentration,
        wavelength_min=200 * u.nm,
        wavelength_max=700 * u.nm,
        reference_atmosphere=None,
        rayleigh_scattering_altitude_bins=RAYLEIGH_SCATTERING_ALTITUDE_BINS,
        write_to_file=True
    ):
        """
        Calculate the absolute integral optical depth due to Rayleigh scattering.

        The optical depth (AOD) for an altitude h over the observatory is given by
        the integral of the monochromatic volume coefficient beta,
        with integration limits h_obs up to h.
        It is provided per altitude bins as a function of wavelength.

        Parameters
        ----------
        rayleigh_extinction_file : string
            Name of the returned file with the extinction profile.
        co2_concentration : float
            12MACOBAC value
        wavelength_min : Quantity
        wavelength_max : Quantity
        reference_atmosphere : path
            The path where the file with the reference atmosphere model is located.
        rayleigh_scattering_altitude_bins : Quantity
            Tuple with the altitudes that the AOD will be calculated. Units of length.
        write_to_file : bool
            If true, the function writes the Rayleigh scattering extinction 
            table into the file `rayleigh_extinction_file`

        Notes
        -----
        This function writes the Rayleigh scattering extinction profile to a file, 
        having ecsv format,  specified by the parameter `rayleigh_extinction_file`.

        Returns
        -------
            Ecsv file with absolute optical depth per altitude bin per wavelength bin.
        """
        m_floor, m_ceiling = self._get_data_altitude_range(
            rayleigh_scattering_altitude_bins
        )
        altitude = rayleigh_scattering_altitude_bins.to(u.km)
        altitude = altitude[altitude < m_ceiling]

        interpolation_centers = (altitude[:-1] + altitude[1:]) / 2
        parameters_dict = self._create_profile(interpolation_centers)
        temperature_lower = parameters_dict["Temperature"]
        relative_humidity_lower = parameters_dict["Relative humidity"]
        pressure_lower = parameters_dict["Pressure"]

        # Concatenate with reference atmosphere
        if reference_atmosphere:
            reference_atmosphere_table = self._pick_up_reference_atmosphere(
                m_ceiling, m_floor, reference_atmosphere
            )
            length_of_columns = len(reference_atmosphere_table)
            relative_humidity_upper = (
                np.zeros(length_of_columns)
                * self.stat_description["avg"]["Relative humidity"].unit
            )
            relative_humidity = np.concatenate(
                (relative_humidity_lower, relative_humidity_upper)
            )
            pressure = np.concatenate(
                (pressure_lower, reference_atmosphere_table["pressure"])
            )
            temperature = np.concatenate(
                (temperature_lower, reference_atmosphere_table["temperature"])
            )
            altitude = np.concatenate(
                (altitude, reference_atmosphere_table["altitude"])
            )
        else:
            logger.warning(
                "Since the reference atmosphere was not provided, "
                "the resulting atmospheric model will be constrained "
                "to the extent of the provided meteorological data."
            )
            temperature = temperature_lower
            pressure = pressure_lower
            relative_humidity = relative_humidity_lower

        t = QTable(
            [altitude[1:], pressure, temperature, relative_humidity],
            names=("altitude", "pressure", "temperature", "relative_humidity"),
        )
        t.sort("altitude")
        bin_widths = np.diff(np.sort(altitude))
        t["bin_widths"] = bin_widths
        mask = t["altitude"] > m_floor
        wavelength_range = (
            np.arange(wavelength_min.to_value(u.nm), wavelength_max.to_value(u.nm), 1)
            * u.nm
        )
        aod_units = len(wavelength_range) * [1 * u.dimensionless_unscaled]
        rayleigh_extinction_table = Table(names=wavelength_range, units=aod_units)
        col_alt_max = Column(name="altitude_max", unit=u.km)
        col_alt_min = Column(name="altitude_min", unit=u.km)
        rayleigh_extinction_table.add_columns(
            [col_alt_max, col_alt_min], indexes=[0, 0]
        )
        aod_dict = {
            aod: 0
            for aod in np.arange(
                wavelength_min.to_value(u.nm), wavelength_max.to_value(u.nm)
            )
        }
        for row in t[mask]:
            new_row = []
            new_row.append(row["altitude"])
            new_row.append(row["altitude"] - row["bin_widths"])
            for wavelength in wavelength_range:
                rayleigh = Rayleigh(
                    wavelength,
                    co2_concentration,
                    row["pressure"],
                    row["temperature"],
                    row["relative_humidity"],
                )
                beta = rayleigh.beta
                aod = row["bin_widths"] * beta
                aod_dict[wavelength.to_value(u.nm)] += aod
                new_row.append(aod_dict[wavelength.to_value(u.nm)])
            rayleigh_extinction_table.add_row(new_row)
        _write(rayleigh_extinction_table, rayleigh_extinction_file)
        return rayleigh_extinction_file

    # pylint: enable=too-many-arguments,too-many-locals

    def convert_to_simtel_compatible(
        self, input_ecsv_file, output_file, observation_altitude
    ):
        """
        Convert extinction profile from ``ecsv`` to ``sim_telarray``-compatible format.

        Parameters
        ----------
        input_ecsv_file : string
            Name of the input extinction profile file in ecsv format.
        output_file : string
            Name of the output extinction profile file in simtel-compatible format.
        observation_altitude : quantity
            Starting altitude measured from sea level.
        """
        extinction_table = QTable.read(input_ecsv_file)
        with open(output_file, "w", encoding="utf-8") as f:
            H2 = observation_altitude.to_value(u.km)
            H1 = extinction_table["altitude_max"].to_value(u.km)
            list_of_altitude_bins = f"# H2= {H2:.3f}, H1= "
            for height in H1:
                list_of_altitude_bins += f"{height:.3f}\t"
            list_of_altitude_bins += "\n"
            f.writelines(list_of_altitude_bins)
            for wl in extinction_table.columns:
                if wl not in ("altitude_max", "altitude_min"):
                    file_line = [str(wl).split(" ", maxsplit=1)[0], "\t"]
                    for aod in extinction_table[wl]:
                        file_line += [f"{aod:.6f}", "\t"]
                    file_line += ["\n"]
                    f.writelines(file_line)

    def timeseries_analysis(
        self,
        outfile,
        altitude_level,
        atmospheric_parameter,
        m_floor,
        m_ceiling,
        altitude_list=STD_CORSIKA_ALTITUDE_PROFILE,
        write_to_file=True,
    ):
        """
        Analyze timeseries of meteorological data.

        Produces an astropy table with the scaled exponential density at 15km a.s.l.
        as a function of the MJD.
        This timeseries is used for the identification of seasons.

        Parameters
        ----------
        outfile : string
            Name of the produced file where the table is stored.
        altitude_level: Quantity
            The altitude level where the timeseries will be created.
            Common choices are 15 km a.s.l, where one can observe the
            maximum difference between seasons, and thus define seasons; another
            common altitude will be the observation level (i.e. surface),
            where one can compare the timeseries obtained
            from a data assimilation system against the local weather station
            of the observatory.
        atmospheric_parameter : string
            The parameter of the timeseries. Common choices are the number density,
            for season definition, and the temperature/pressure/relative humidity,
            for DAS validation.
        altitude_list : Quantity
            Tuple with the altitudes that the atmospheric parameters will be calculated.
            Units of length.
        m_floor: Quantity
            Lowest altitude considered in calculations.
        m_ceiling: Quantity
            Highest altitude considered in calculations.
        write_to_file : bool
            If true the function writes the timeseries into the file 'outfile'

        Notes
        -----
        This function writes the data timeseries to a file, having ecsv format, 
        specified by the parameter `outfile`.
        """
        tables = []
        altitude = altitude_list[
            (altitude_list.to_value() >= m_floor.to_value(altitude_list.unit))
            & (altitude_list.to_value() < m_ceiling.to_value(altitude_list.unit))
        ]

        self.data["MJD"] = self.data["Timestamp"].mjd
        test_table = self.data.group_by("MJD")
        indices = test_table.groups.indices
        for first, second in zip(indices, indices[1:]):
            t = test_table[first:second]
            parameter = (
                self._interpolate(
                    t["Altitude"],
                    t[atmospheric_parameter],
                    altitude,
                )
                * t[atmospheric_parameter].unit
            )
            current_table = QTable(
                [parameter, altitude], names=(atmospheric_parameter, "altitude")
            )
            current_table["mjd"] = t["MJD"][1]
            mask = current_table["altitude"] == altitude_level
            tables.append(current_table[mask])
        output_table = vstack(tables)
        _write(output_table, outfile)
        del tables

    # pylint: enable=too-many-locals

    def molecular_extinction_profile(
        self, rayleigh_extinction_file, 
        molecular_absorption_file, 
        mep_file,
        write_to_file=True,
    ):
        """
        Produce a Molecular Extinction Profile (MEP).

        MEP combines the
        extinction due to Rayleigh scattering with the absorption due to ozone.
        Ozone features the dominant molecular absorption in the wavelengths of
        interest. Contributions from other molecules might be added in the future.

        Parameters
        ----------
        rayleigh_extinction_file : file
            Ecsv file with absolute optical depth due to Rayleigh scatteringper
            altitude bin per wavelength bin. Alternatively, in case of a
            dedicated study, one would pass a different extinction file,
            e.g. of a given molecule.
        molecular_absorption_file : file
            Ecsv file with absolute optical depth due to molecular absorption per
            altitude bin per wavelength bin.
        mep_file : string
            Name of the produced file where the MEP is stored.
        write_to_file : true
            If true, the function writes the MEP into the file `mep_file`.

        Notes
        -----
        This function writes the MEP to a file, having ecsv format, 
        specified by the parameter `mep_file`.

        Returns
        -------
            Astropy table with a MEP, featuring the absolute optical depth
            per altitude bin per wavelength bin.
        """
        molecular_extinction_table = Table.read(rayleigh_extinction_file)
        molecular_absorption_table = Table.read(molecular_absorption_file)
        for col_ozone, col_rs in zip(
            molecular_absorption_table.columns, molecular_extinction_table.columns
        ):
            if col_ozone != "altitude_max" and col_ozone != "altitude_min":
                molecular_extinction_table[col_rs] = (
                    molecular_absorption_table[col_ozone]
                    + molecular_extinction_table[col_rs]
                )
        _write(molecular_extinction_table, mep_file)
        return molecular_extinction_table

    def molecular_absorption(
        self,
        molecule_name,
        molecular_absorption_file,
        molecule_cross_section_file,
        molar_mass=MOLAR_MASS_OZONE,
        wavelength_min=200 * u.nm,
        wavelength_max=700 * u.nm,
        rayleigh_scattering_altitude_bins=RAYLEIGH_SCATTERING_ALTITUDE_BINS,
        write_to_file=True,
    ):
        """
        Produce a Molecular Absorption Profile (MAP).

        Calculates the optical depth due to molecular absorption
        per altitude bins as a function of wavelength. In order to
        calculate the optical depth, it multiplies the absorption cross section
        (which is a function of wavelength) to the number density of the respective
        molecule (which is a function of altitude). 

        Parameters
        ----------
        molecule_name : string
            Name of the required molecule
        molecular_absorption_file : string
            Name of the file where the MAP is stored.
        molecule_cross_section_file : string
            Name of the file storing the molecule's absorption cross section.
        wavelength_min : Quantity
        wavelength_max : Quantity
        rayleigh_scattering_altitude_bins : Quantity
            Tuple with the altitudes that the AOD will be calculated. Units of length.
        molar_mass : Quantity
            The molar mass of the studied molecule.
        write_to_file : bool
            If true, the function writes the MAP into the `molecular_absorption_file`

        Notes
        -----
        This function writes the MAP to a file, having ecsv format, 
        specified by the parameter `molecular_absorption_file`.

        Returns
        -------
            Astropy with the molecular absorption optical depth per altitude bin
        per wavelength bin.
        """
        altitude = rayleigh_scattering_altitude_bins.to(u.km)
        interpolation_centers = (altitude[:-1] + altitude[1:]) / 2
        parameters_dict = self._create_profile(interpolation_centers)
        mixing_ratio_parameter_name = f"{molecule_name} mass mixing ratio"
        molecule_mixing_ratio = parameters_dict[mixing_ratio_parameter_name]
        mass_density = parameters_dict["Density"] / N0_AIR
        molecule_mixing_ratio[np.isnan(molecule_mixing_ratio)] = 0
        mass_density[np.isnan(mass_density)] = 0

        cross_section_table = self._interpolate_cross_section(
            molecule_cross_section_file
        )

        molecule_profile_table = QTable(
            [altitude[1:], mass_density.to(u.g / u.cm**3), molecule_mixing_ratio],
            names=("altitude", "density", "mixing_ratio"),
        )
        molecule_profile_table["number_density"] = (
            molecule_profile_table["mixing_ratio"]
            * molecule_profile_table["density"]
            * (N_A / molar_mass)
        ).decompose()
        molecule_profile_table.sort("altitude")
        bin_widths = np.diff(np.sort(altitude))
        molecule_profile_table["bin_widths"] = bin_widths

        wavelength_range = self._wavelength_range(wavelength_min, wavelength_max)
        molecular_absorption_table = Table(names=wavelength_range)
        col_alt_max = Column(name="altitude_max", unit=u.km)
        col_alt_min = Column(name="altitude_min", unit=u.km)
        molecular_absorption_table.add_columns(
            [col_alt_max, col_alt_min], indexes=[0, 0]
        )
        aod_dict = {aod: 0 for aod in wavelength_range.to_value(u.nm)}
        for row in molecule_profile_table:
            new_row = []
            new_row.append(row["altitude"])
            new_row.append(row["altitude"] - row["bin_widths"])
            for wavelength in wavelength_range:
                mask = cross_section_table["wavelength"] == wavelength
                cross_section_table_masked = cross_section_table[mask]
                beta = (
                    row["number_density"] * cross_section_table_masked["cross section"]
                )
                beta = beta.decompose()
                if np.isnan(beta):
                    beta = 0
                aod = row["bin_widths"].to(u.m) * beta
                aod_dict[wavelength.to_value(u.nm)] += aod
                new_row.append(aod_dict[wavelength.to_value(u.nm)])
            molecular_absorption_table.add_row(new_row)
        _write(molecular_absorption_table, molecular_absorption_file)

        return molecular_absorption_table
