"""
DOCSTRING
"""

import data_loading as dl
from config import TorontoConfig
from entities import *


class PreprocessingSystem:
    """
    Class to manage all preprocessing of data for a model.

    Instance Attributes:
        - start_date: the earliest that will be included in the model.
        - end_date: the final date that will be included in the model.
        - regions: a dictionary mapping the name of a region to an instance of a Region.

    """
    regions: dict[str: SuperRegion]

    def __init__(self) -> None:
        self.regions = {}

    def init_toronto_model(self) -> None:
        """
        Initialise classes for toronto model.
        """

        config = TorontoConfig()

        data_loading_system = dl.DataLoadingToronto(config.start_date, config.end_date)
        self.regions['Toronto'] = data_loading_system.load_super_region(config.paths['regions'])

        neighbourhoods = data_loading_system.load_sub_regions(config.paths['regions'])

        for neighbourhood in neighbourhoods.values():
            self.regions['Toronto'].add_sub_region(neighbourhood)
