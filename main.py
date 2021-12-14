"""
DOCSTRING

TODO: main run file
"""

import modules.preprocessing as p
import modules.visualizer as v
import requests
from modules.data_collection import scrape_incomes


def obtain_data() -> None:
    """
    Obtains data from the web to be modelled.
    """
    scrape_incomes()


def generate_model() -> None:
    """ Generates a covid/socioeconomic economic model for Toronto and displays visuals  """
    preprocessing_system = p.PreprocessingSystem()
    preprocessing_system.init_toronto_model()
    visual_system = v.RegionVisual(preprocessing_system)
    visual_system.toronto_scatter_visual()
    visual_system.toronto_heatmap('Covid')
    visual_system.toronto_heatmap('Income')


go_ahead = input('Has the toronto_covid_cases.csv file been downloaded and pot into the'
                 ' correct directory? (CovidSocioeconomicModel/data/toronto_covidcases/.csv) Y/N?')
obtain_data()
generate_model()
