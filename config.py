"""
DOCSTRING
"""

import datetime


class TorontoConfig:
    """
    Class containing config info for Toronto model.
    """
    start_date: datetime.date

    def __init__(self) -> None:

        self.start_date = datetime.date(2021, 3, 1)
        self.end_date = datetime.date(2021, 11, 1)

        self.paths = {
            'regions': 'data/toronto_regions.csv'
        }
