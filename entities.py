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
    num_cases: int
    super_region: SuperRegion
    median_household_income: int
    scaled_economic_index: float
    scaled_case_index: float

    def __init__(self, name: str, population: int, super_region: SuperRegion, median_household_income: int) -> None:
        super().__init__(name, population)
        self.super_region = super_region
        self.cases = {}
        self.num_cases = 0
        self.median_household_income = median_household_income
        self.scaled_economic_index = 0
        self.scaled_case_index = 0

    def add_covid_case(self, covid_case: CovidCase) -> bool:
        """
        Adds a covid case to a sub region if it is not already added. Returns whether the sub region
        is successfully added.
        """
        if covid_case.case_id in self.cases.keys():
            return False
        else:
            self.cases[covid_case.case_id] = covid_case
            self.num_cases = len(self.cases)
            return True


class SuperRegion(Region):
    """
    Abstract data class to represent a super region.

    Representation Invariant:
        - sum(subregion.population for subregion in self.sub_regions) == self.population

    """

    _sub_regions: dict[str: SubRegion]
    economic_multiplier: float
    max_household_income: int
    min_household_income: int
    case_multiplier: float
    max_num_cases: int
    min_num_cases: int

    def __init__(self, name: str, population: int) -> None:
        super().__init__(name, population)
        self._sub_regions = {}
        self.update_economic_scaling()
        self.update_case_scaling()

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

    def update_economic_scaling(self) -> float:
        """
        Update the economic scaling of the super region and its subregions. Returns the economic scaling multiplier.
        """
        household_incomes = {sub_region.median_household_income for sub_region
                             in self._sub_regions.values()}

        if len(household_incomes) >= 2:
            self.max_household_income = max(household_incomes)
            self.min_household_income = min(household_incomes)
            self.economic_multiplier = 10 / (self.max_household_income - self.min_household_income)
        elif len(household_incomes) == 1:
            self.max_household_income = max(household_incomes)
            self.min_household_income = min(household_incomes)
            self.economic_multiplier = 0
        else:
            self.max_household_income = 0
            self.min_household_income = 0
            self.economic_multiplier = 0

        for sub_region in self._sub_regions.values():
            sub_region.scaled_economic_index = self.calculate_scaled_economic_index(
                sub_region.median_household_income)

        return self.economic_multiplier

    def calculate_scaled_economic_index(self, household_income: int) -> float:
        """
        Return the scaled economic index for the sub region.
        """

        return (household_income - self.min_household_income) * self.economic_multiplier

    def update_case_scaling(self) -> float:
        """
        Update the case scaling of the super region and its subregions. Returns the case scaling multiplier.
        """
        all_num_cases = {sub_region.num_cases for sub_region in self._sub_regions.values()}

        if len(all_num_cases) >= 2:
            self.max_num_cases = max(all_num_cases)
            self.min_num_cases = min(all_num_cases)
            self.case_multiplier = 10 / (self.max_num_cases - self.min_num_cases)
        elif len(all_num_cases) == 1:
            self.max_num_cases = max(all_num_cases)
            self.min_num_cases = min(all_num_cases)
            self.case_multiplier = 0
        else:
            self.max_num_cases = 0
            self.min_num_cases = 0
            self.case_multiplier = 0

        for sub_region in self._sub_regions.values():
            sub_region.scaled_case_index = self.calculate_scaled_case_index(
                sub_region.num_cases)

        return self.case_multiplier

    def calculate_scaled_case_index(self, num_cases: int) -> float:
        """
        Return the scaled case index for the sub region.
        """

        return (num_cases - self.min_num_cases) * self.case_multiplier


class Neighbourhood(SubRegion):
    """
    Class to represent a neighbourhood.
    """

    def __init__(self, name: str, population: int, city: City, median_household_income: int) -> None:
        super().__init__(name, population, city, median_household_income)


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
