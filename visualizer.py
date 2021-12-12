""" Visualizes covid data for a given system """
from preprocessing import PreprocessingSystem
import pandas as pd
import matplotlib


class RegionVisual:
    """ Creates a shapely visual of different attributes of a region"""
    system: PreprocessingSystem

    def __init__(self, system: PreprocessingSystem):
        self.system = system

    def scatter_visual(self) -> None:
        """ Creates a scatter plot comparing subregions income against covid cases """
        data = {'Cases': [], 'Income': []}
        toronto = self.system.regions['Toronto']
        hoods = toronto.neighbourhoods
        for subregion in hoods:
            data['Cases'].append(len(hoods[subregion].cases) / hoods[subregion].population)
            data['Income'].append(hoods[subregion].median_household_income)
        df = pd.DataFrame(data)
        df.plot.scatter(x='Income', y='Cases')


def do_the_thing():
    p = PreprocessingSystem()
    p.init_toronto_model()
    r = RegionVisual(p)
    r.scatter_visual()
