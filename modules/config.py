"""
DOCSTRING
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

        self.start_date = datetime.date(2020, 12, 1)
        self.end_date = datetime.date(2021, 3, 1)

        self.paths = {
            'regions': 'data/toronto_regions.csv',
            'cases': 'data/toronto_covid_cases.csv'
        }
        self.regression = {
            'angle_divisor': 1000
        }
