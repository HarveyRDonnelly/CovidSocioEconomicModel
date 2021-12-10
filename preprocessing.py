"""
DOCSTRING
"""

import datetime


class Region:
    """
    Abstract data class to represent a sub region.
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


class City(SuperRegion):
    """
    Class to represent a neighbourhood within a region.
    """


class Neighbourhood(SubRegion):
    """
    Class to represent a neighbourhood within a region.
    """


class PreprocessingSystem:
    """
    Class to manage all preprocessing of data for a model.

    Instance Attributes:
        - start_date: the earliest that will be included in the model.
        - end_date: the final date that will be included in the model.
        - regions: a dictionary mapping the name of a region to an instance of a Region.

    """
    start_date: datetime.datetime
    end_date: datetime.datetime
    regions: dict[str: Region]
