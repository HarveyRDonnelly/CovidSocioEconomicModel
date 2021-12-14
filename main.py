"""
Module Name: Main Module
Source Path: main.py

Description:

This python module runs the entire project. First it obtains necessary data, then it generates a
model of the processing system, which in turn produces visuals for the model.

===============================

CSC110 Final Project:

"Virus of Inequality: The Socio-Economic Disparity of COVID-19 Cases
in the City of Toronto"

This file is Copyright (c) 2021 Harvey Ronan Donnelly and Ewan Robert Jordan.
"""

import modules.preprocessing as p
import modules.visualizer as v
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
if go_ahead.lower() == 'y':
    print('Running project...')
    # obtain_data()
    generate_model()
    print('Model Generate and Visualized.')
else:
    print('Ok, rerun this file once proper files have been downloaded')
