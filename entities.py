"""
DOCSTRING
"""

from __future__ import annotations
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

    cases: dict[int, CovidCase]
    super_region: SuperRegion

    def __init__(self, name: str, population: int, super_region: SuperRegion) -> None:
        super().__init__(name, population)
        self.super_region = super_region
        self.cases = {}

    def add_covid_case(self, covid_case: CovidCase) -> bool:
        """
        Adds a covid case to a sub region if it is not already added. Returns whether the sub region
        is successfully added.
        """
        if covid_case.case_id in self.cases.keys():
            return False
        else:
            self.cases[covid_case.case_id] = covid_case
            return True


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

    def __init__(self, name: str, population: int, city: City, median_household_income: int) -> None:
        super().__init__(name, population, city)
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

    case_id: int
    date: datetime.date
    super_region: SuperRegion
    sub_region: SubRegion

    def __init__(self, case_id: int, date: datetime.date, super_region: SuperRegion, sub_region: SubRegion):
        self.case_id = case_id
        self.date = date
        self.super_region = super_region
        self.sub_region = sub_region