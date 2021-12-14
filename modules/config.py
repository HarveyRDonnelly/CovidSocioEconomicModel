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
            'regions': 'data/pregenerated/pregenerated_toronto_regions.csv',
            'cases': 'data/pregenerated_toronto_covid_cases.csv',
            'shapes': 'data/pregenerated/pregenerated_toronto_boundaries/Neighbourhoods.shp'
        }
        self.regression = {
            'angle_divisor': 1000
        }
