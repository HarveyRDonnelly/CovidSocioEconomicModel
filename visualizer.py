""" Visualizes covid data for a given system """
from preprocessing import PreprocessingSystem
import pandas as pd


class RegionVisual:
    """ Creates a shapely visual of different attributes of a region"""
    system: PreprocessingSystem

    def __init__(self, system: PreprocessingSystem):
        self.system = system

    def scatter_visual(self) -> None:
        """ Creates a scatter plot comparing subregions income against covid cases """
        data = {'Cases': [], 'Income': []}
        toronto = self.system.regions['Toronto']
        for subregion in toronto.neighbourhood:
            data['Cases'].append(subregion.cases/subregion.population)
            data['Income'].append(subregion.median_household_income)
            df = pd.DataFrame(data)
            df.plot.scatter()





