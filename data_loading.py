"""
DOCSTRING
"""
import csv
import datetime

from entities import *


# Data Formatting Functions

def remove_commas_number_string(number_string: str) -> int:
    """
    Returns an integer from a string representing a number with commas.

    >>> number = "56,987"
    >>> remove_commas_number_string(number)
    56987
    """
    formatted_number = number_string.replace(',', '')
    formatted_number = formatted_number.replace(' ', '')

    return int(formatted_number)


# Data Loading System Classes

class DataLoadingSystem:
    """
    Abstract class containing methods to load data for regions and subregions.
    """

    start_date: datetime.date
    end_date: datetime.date

    def __init__(self, start_date: datetime.date, end_date: datetime.date):
        self.start_date = start_date
        self.end_date = end_date

    def load_super_region(self, path: str) -> None:
        """
        Method to load data for super region from a file.
        """
        raise NotImplementedError

    def load_sub_regions(self, path: str) -> None:
        """
        Method to load data for all sub regions from a file.
        """
        raise NotImplementedError

    def load_covid_cases(self, path: str) -> None:
        """
        Method to load data for all covid cases from a file.
        """
        raise NotImplementedError


class DataLoadingToronto(DataLoadingSystem):
    """
    Concrete class containing methods to load data for Toronto and its Neighbourhoods.
    """

    def __init__(self, start_date: datetime.date, end_date: datetime.date):
        super().__init__(start_date, end_date)

    def load_super_region(self, path: str) -> City:
        """
        Method to load data for super regions from a file.
        """
        with open(path) as dataset:
            reader = csv.reader(dataset, delimiter=',')
            next(reader)  # Skip the dataset's header.

            rows = [row for row in reader]

            city_row = rows[0]
            name = city_row[0]
            population = remove_commas_number_string(city_row[1])

            city = City(name, population)

        return city

    def load_sub_regions(self, path: str) -> dict[str, Neighbourhood]:
        """
        Method to load data for all sub regions from a file.
        """
        with open(path) as dataset:
            reader = csv.reader(dataset, delimiter=',')
            next(reader)  # Skip the dataset's header.
            next(reader)  # Skip the entry for City of Toronto.

            neighbourhoods = {}

            for row in reader:
                name = row[0]
                population = remove_commas_number_string(row[1])
                median_household_income = remove_commas_number_string(row[2])
                neighbourhoods[name] = Neighbourhood(name, population, median_household_income)

        return neighbourhoods

    def load_covid_cases(self, path: str) -> None:
        """
        Method to load data for all sub regions from a file.
        """
        raise NotImplementedError
