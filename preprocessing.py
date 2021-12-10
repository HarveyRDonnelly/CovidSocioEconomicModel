"""
DOCSTRING
"""

import data_loading as dl
from config import TorontoConfig


class Region:
    """
    Abstract data class to represent a sub region.

    Instance Attributes:
        - name: the name of the region.
        - population: the population of the region.

    """

    name: str
    population: int

    def __init__(self, name, population) -> None:
        self.name = name
        self.population = population


class SubRegion(Region):
    """
    Abstract data class to represent a sub region.
    """

    def __init__(self, name: str, population: int) -> None:
        super().__init__(name, population)


class SuperRegion(Region):
    """
    Abstract data class to represent a super region.

    Representation Invariant:
        - sum(subregion.population for subregion in self.sub_regions) == self.population

    """

    _sub_regions: dict[str: SubRegion]

    def __init__(self, name: str, population: int) -> None:
        super().__init__(name, population)
        self._sub_regions = {}

    def add_sub_region(self, subregion: SubRegion) -> bool:
        """
        Add subregion to subregion dictionary if subregion is not already added. Return whether the
        subregion is added.
        """
        if subregion.name in self._sub_regions:
            return False
        else:
            self._sub_regions[subregion.name] = subregion
            return True


class Neighbourhood(SubRegion):
    """
    Class to represent a neighbourhood.
    """

    median_household_income: int

    def __init__(self, name: str, population: int, median_household_income: int) -> None:
        super().__init__(name, population)
        self.median_household_income = median_household_income


class City(SuperRegion):
    """
    Class to represent a city.
    """

    def __init__(self, name: str, population: int) -> None:
        super().__init__(name, population)

    def add_sub_region(self, neighbourhood: Neighbourhood) -> bool:
        """
        Add subregion to subregion dictionary if subregion is not already added. Return whether the
        subregion is added.
        """
        return super().add_sub_region(neighbourhood)


class PreprocessingSystem:
    """
    Class to manage all preprocessing of data for a model.

    Instance Attributes:
        - start_date: the earliest that will be included in the model.
        - end_date: the final date that will be included in the model.
        - regions: a dictionary mapping the name of a region to an instance of a Region.

    """
    regions: dict[str: SuperRegion]

    def __init__(self) -> None:
        self.regions = {}

    def init_toronto_model(self) -> None:
        """
        Initialise classes for toronto model.
        """

        config = TorontoConfig()

        data_loading_system = dl.DataLoadingToronto(config.start_date, config.end_date)
        self.regions['Toronto'] = data_loading_system.load_super_region(config.paths['regions'])

        neighbourhoods = data_loading_system.load_sub_regions(config.paths['regions'])

        for neighbourhood in neighbourhoods.values():
            self.regions['Toronto'].add_sub_region(neighbourhood)
