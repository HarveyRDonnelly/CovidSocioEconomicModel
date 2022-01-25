"""
Module Title: Data Loading Module
Source Path: modules/data_loading.py

Description:

The Data Loading Module is responsible for loading raw data from external files (such as .csv) into
the appropriate class entities for the project. The module currently only contains a concrete
implementation of a data loading class for the City of Toronto (DataLoadingToronto). However, this
module is designed using abstract classes so that further concrete implementations of the
DataLoadingSystem can be easily added in the future to investigate the same trends in different
urban regions (i.e. super-regions).

The Data Loading Module also contains  helper functions that are used for cleaning and manipulating
data as required in the project.

===============================

CSC110 Final Project:

"Virus of Inequality: The Socio-Economic Disparity of COVID-19 Cases
in the City of Toronto"

This file is Copyright (c) 2021 Harvey Ronan Donnelly and Ewan Robert Jordan.

"""
import csv
from modules.entities import *



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


def string_to_datetime(date_string: str) -> datetime.date:
    """
    Returns a datetime.date from a string representing a date in the format YYYY-MM-DD.

    >>> string = "2020-03-02"
    >>> output = string_to_datetime(string)
    >>> output == datetime.date(2020, 3, 2)
    True
    """
    split_string = date_string.split('-')
    year = int(split_string[0])
    month = int(split_string[1])
    day = int(split_string[2])

    return datetime.date(year, month, day)


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

    def load_sub_regions(self, path: str, super_region: SuperRegion) -> None:
        """
        Method to load data for all sub regions from a file.
        """
        raise NotImplementedError

    def load_covid_cases(self, path: str, subregion: SubRegion) -> None:
        """
        Method to load data for all covid cases for a subregion.
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
        Method to load data for the City of Toronto super region from a file.
        """
        print('[modules.data_loading] Opening Toronto Region Dataset')
        with open(path) as dataset:
            reader = csv.reader(dataset, delimiter=',')
            next(reader)  # Skip the dataset's header.

            rows = [row for row in reader]

            city_row = rows[0]
            name = city_row[0]
            population = remove_commas_number_string(city_row[1])

            city = City(name, population)

        return city

    def load_sub_regions(self, path: str, city: City) -> dict[str, Neighbourhood]:
        """
        Method to load data for all neighbourhoods in the City of Toronto from a file.
        """
        print('[modules.data_loading] Extracting individual subregion data .')
        with open(path) as dataset:
            reader = csv.reader(dataset, delimiter=',')
            next(reader)  # Skip the dataset's header.
            next(reader)  # Skip the entry for City of Toronto.

            neighbourhoods = {}

            for row in reader:
                name = row[0]
                population = remove_commas_number_string(row[1])
                median_household_income = remove_commas_number_string(row[2])
                neighbourhoods[name] = Neighbourhood(name, population, city,
                                                     median_household_income)
                print('[modules.data_loading] Neighbourhood Added:' + name)

        return neighbourhoods

    def load_covid_cases(self, path: str, neighbourhood: Neighbourhood) -> dict[int, CovidCase]:
        """
        Method to load all covid cases for a specified neighbourhood.
        """
        print('[modules.data_loading] Opening covid case files')
        with open(path) as dataset:
            reader = csv.reader(dataset, delimiter=',')
            next(reader)  # Skip the dataset's header.

            cases = {}
            for row in reader:
                if self.start_date <= string_to_datetime(row[9]) <= self.end_date and neighbourhood.name == row[4]:
                    case_id = int(row[0])
                    date = string_to_datetime(row[9])
                    super_region = neighbourhood.super_region
                    sub_region = neighbourhood
                    cases[case_id] = CovidCase(case_id, date, super_region, sub_region)
                    print('[modules.data_loading] Covid Case added id#:' + str(case_id))

        return cases


if __name__ == '__main__':
    import python_ta.contracts

    python_ta.contracts.DEBUG_CONTRACTS = False
    python_ta.contracts.check_all_contracts()

    import doctest

    doctest.testmod(verbose=True)

    import python_ta

    python_ta.check_all(config={
        'extra-imports': ['csv', 'modules.entities'],
        'allowed-io': ['load_super_region', 'load_covid_cases', 'load_sub_region'],
        'max-line-length': 100,
        'disable': ['R1705', 'C0200']
    })
