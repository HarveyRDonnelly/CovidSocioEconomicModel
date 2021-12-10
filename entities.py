"""
DOCSTRING
"""

import datetime

# Region entities


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

    neighbourhoods: dict[str, Neighbourhood]

    def __init__(self, name: str, population: int) -> None:
        super().__init__(name, population)
        self.neighbourhoods = self._sub_regions

    def add_sub_region(self, neighbourhood: Neighbourhood) -> bool:
        """
        Add subregion to subregion dictionary if subregion is not already added. Return whether the
        subregion is added.
        """
        return super().add_sub_region(neighbourhood)


# Covid Case entities

class CovidCase:
    """
    Class to represent a covid case.
    """

    date: datetime.date
    super_region: None
    sub_region: None
