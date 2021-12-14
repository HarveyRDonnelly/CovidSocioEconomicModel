"""
Module Name: Preprocessing Module
Source Path: modules/preprocessing.py

Description:

This python module contains a concrete class which manages the creation of the project's
data system. It is made to support the initialization of many different regions' covid/income data,
but only has the city of Toronto implemented. This class also is in charge of calling the regression
module onto a certain region.
"""

from modules import data_loading as dl
from modules.config import TorontoConfig
from modules.entities import *
from modules.regression import ExponentialRegressionModel


class PreprocessingSystem:
    """
    Class to manage all preprocessing of data for a model.

    Instance Attributes:
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

        neighbourhoods = data_loading_system.load_sub_regions(config.paths['regions'],
                                                              self.regions['Toronto'])

        for neighbourhood in neighbourhoods.values():
            self.regions['Toronto'].add_sub_region(neighbourhood)
            neighbourhood_cases = data_loading_system.load_covid_cases(config.paths['cases'],
                                                                       neighbourhood)
            for case in neighbourhood_cases.values():
                neighbourhood.add_covid_case(case)

        self.regions['Toronto'].update_economic_scaling()
        self.regions['Toronto'].update_case_scaling()

        self.toronto_model_regression()

    def toronto_model_regression(self) -> None:
        """
        Generates exponential regression model for toronto data.
        """

        config = TorontoConfig()

        coordinates = [(neighbourhood.scaled_economic_index, neighbourhood.scaled_case_index)
                       for neighbourhood in self.regions['Toronto'].neighbourhoods.values()]

        self.regions['Toronto'].regression_model = ExponentialRegressionModel(coordinates,
                                                                              config.regression['angle_divisor'])
