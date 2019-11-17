# -*- coding: utf-8 -*-
# from pydash import has, get
from enum import Enum
from typing import List
from typing import Optional

import csdmpy as cp
from astropy import units as u
from mrsimulator import Dimension
from mrsimulator import Isotopomer
from mrsimulator.importer import import_json
from mrsimulator.sandbox import AveragingScheme
from pydantic import BaseModel
from pydantic import Field

__author__ = "Deepansh J. Srivastava"
__email__ = ["srivastava.89@osu.edu", "deepansh2012@gmail.com"]


class IntegrationVolumeEnum(str, Enum):
    octant = "octant"
    hemisphere = "hemisphere"


class ConfigSimulator(BaseModel):
    """
    The configurable parametes used in lineshape simulation

    Attributes:
        number_of_sidebands: The number of sidebands requested for simulation
        integration_volume: An enumeration ('octant', 'hemisphere') over which the
            lineshape average is evaluated.
        integration_density: This number is used to evaluate the number of orientations
            at which the frequencies are calculated. If `n` is the integration_density,
            then the number of orientations are ``(n+1)*(n+2)/2 * number of octant``.

    Example:
        >>> a = Simulator()
        >>> a.config.number_of_sidebands = 128
        >>> a.config.integration_volume = 'hemisphere'
    """

    number_of_sidebands: int = Field(64, ge=1)
    integration_volume: IntegrationVolumeEnum = IntegrationVolumeEnum.octant
    integration_density: int = Field(70, ge=1)
    _averaging_scheme: Optional[AveragingScheme] = None
    # previous_integration_volume: ClassVar[int] = None
    # previous_integration_density: ClassVar[str] = None

    class Config:
        validate_assignment = True
        arbitrary_types_allowed = True
        # fields = {"_previous_integration_volume": "previous_integration_volume"}
        # fields = {"_previous_integration_density": "previous_integration_density"}

    def __post_init__(self):
        print(self.integration_density, self.integration_volume.value)
        self._averaging_scheme = AveragingScheme(
            integration_density=self.integration_density,
            integration_volume=self.integration_volume.value,
            allow_fourth_rank=True,
        )

    @property
    def averaging_scheme(self):
        return self._averaging_scheme

    # @property
    # def averaging_scheme(self):
    #     # if (
    #     #     self.previous_integration_volume == self.integration_volume
    #     #     and self.previous_integration_density == self.integration_density
    #     # ):
    #     #     return

    #     return AveragingScheme(
    #         integration_density=self.integration_density,
    #         integration_volume=self.integration_volume.value,
    #         allow_fourth_rank=True,
    #     )
    # self.previous_integration_volume = self.integration_volume
    # self.previous_integration_density = self.integration_density


class Simulator(BaseModel):
    """
    The simulator class.

    Attributes:
        isotopomers: List of :ref:`isotopomer_api` objects.
        dimensions: List of :ref:`dimension_api` objects.
        config: :ref:`config_api` object.
    """

    isotopomers: List[Isotopomer] = []
    dimensions: List[Dimension] = []
    simulated_data: Optional[List]
    config: ConfigSimulator = ConfigSimulator()

    class Config:
        validate_assignment = True

    def get_isotopes(self, I=None):
        """
        Set of unique isotopes from sites in the list of isotopomers corresponding
        to spin quantum number `I`. If `I` is unspecified or None, a set of all
        unique isotopes is returned instead.

        Args:
            I: (optional) The spin quantum number. Valid input are multiples of 0.5.

        Returns:
            A Set

        Example:
            >>> sim.get_isotopes() # doctest:+SKIP
            {'1H', '27Al', '13C'}
            >>> sim.get_isotopes(I=0.5) # doctest:+SKIP
            {'1H', '13C'}
            >>> sim.get_isotopes(I=1.5)
            set()
            >>> sim.get_isotopes(I=2.5)
            {'27Al'}
        """
        st = set()
        for isotopomer in self.isotopomers:
            st.update(isotopomer.get_isotopes(I))
        return st

    def load_isotopomers(self, filename):
        """
        Load a list of isotopomers from JSON serialized isotopomers file.

        See an
        `example <https://raw.githubusercontent.com/DeepanshS/mrsimulator-test
        /master/isotopomers_ppm.json>`_
        of JSON serialized isotopomers file. For details, refer to the
        :ref:`load_isotopomers` section.

        Args:
            `filename`: A local or remote address to the JSON serialized isotopomers
                        file.
        """
        contents = import_json(filename)
        json_data = contents["isotopomers"]
        self.isotopomers = [Isotopomer.parse_dict_with_units(obj) for obj in json_data]

    def run(self, method, **kwargs):
        """Simulate the lineshape.

        Args:
            method: The methods used in simulating line-shapes.
        """
        isotopomers = [
            isotopomer.to_freq_dict(self.dimensions[0].magnetic_flux_density)
            for isotopomer in self.isotopomers
        ]

        amp = method(dimension=self.dimensions, isotopomers=isotopomers, **kwargs)

        if isinstance(amp, list):
            self.simulated_data = amp
        else:
            self.simulated_data = [amp]

        """The frequency is in the units of Hz."""
        freq = self.dimensions[0].coordinates_ppm
        freq *= u.Unit("ppm")
        return freq, amp

    def as_csdm_object(self):
        """
        Converts the data to a CSDM object. Read
        `csdmpy <https://csdmpy.readthedocs.io/en/latest/>`_ for details

        Return:
            CSDM object
        """
        new = cp.new()
        for dimension in self.dimensions:
            new_dimension = {
                "type": "linear",
                "count": dimension.number_of_points,
                "increment": "{0} Hz".format(
                    dimension.spectral_width / dimension.number_of_points
                ),
                "coordinates_offset": f"{dimension.reference_offset} Hz",
                "origin_offset": f"{dimension.larmor_frequency} Hz",
                "complex_fft": True,
            }
            new.add_dimension(new_dimension)

        dependent_variable = {
            "type": "internal",
            "quantity_type": "scalar",
            "numeric_type": "float64",
        }
        for index, datum in enumerate(self.simulated_data):
            if datum != []:
                dependent_variable["components"] = [datum]
                name = self.isotopomers[index].name
                if name != "":
                    dependent_variable.update({"name": name})

                description = self.isotopomers[index].description
                if description != "":
                    dependent_variable.update({"description": description})

                dependent_variable["application"] = {
                    "com.github.DeepanshS.mrsimulator": {
                        "isotopomers": [self.isotopomers[index].to_dict_with_units()]
                    }
                }
                new.add_dependent_variable(dependent_variable)
                new.dependent_variables[-1].encoding = "base64"
        return new
