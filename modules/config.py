"""
Module Name: Configuration Module
Source Path: modules/config.py

Description:

This module contains a class which contains important configuration variables as attributes,
including file paths and starting date and ending date for covid case usage.

===============================

CSC110 Final Project:

"Virus of Inequality: The Socio-Economic Disparity of COVID-19 Cases
in the City of Toronto"

This file is Copyright (c) 2021 Harvey Ronan Donnelly and Ewan Robert Jordan.
"""

import datetime


class TorontoConfig:
    """
    Class containing config info for Toronto model.
    """
    start_date: datetime.date
    end_date: datetime.date
    paths: dict[str, str]
    regression: dict[str, any]

    def __init__(self) -> None:

        self.start_date = datetime.date(2020, 9, 1)
        self.end_date = datetime.date(2021, 12, 1)

        self.paths = {
            'regions': 'data/toronto_regions.csv',
            'cases': 'data/toronto_covid_cases.csv',
            'shapes': 'data/toronto_boundaries/Neighbourhoods.shp'
        }
        self.regression = {
            'angle_divisor': 1000
        }


if __name__ == '__main__':
    import python_ta.contracts

    python_ta.contracts.DEBUG_CONTRACTS = False
    python_ta.contracts.check_all_contracts()

    import doctest

    doctest.testmod(verbose=True)

    import python_ta

    python_ta.check_all(config={
        'extra-imports': ['datetime'],
        'allowed-io': [],
        'max-line-length': 100,
        'disable': ['R1705', 'C0200']
    })
