""" Visualizes covid data for a given system """
from preprocessing import PreprocessingSystem
from regression import ExponentialRegressionModel
import pandas as pd
from string import digits
import matplotlib
import numpy as np
import shapefile as shp
import matplotlib.pyplot as plt
import seaborn as sns
import os


class RegionVisual:
    """ Creates a shapely visual of different attributes of a region"""
    system: PreprocessingSystem

    def __init__(self, system: PreprocessingSystem):
        self.system = system

    def toronto_scatter_visual(self) -> None:
        """ Creates a scatter plot comparing subregions income against covid cases """
        data = {'Cases': [], 'Income': []}
        toronto = self.system.regions['Toronto']
        hoods = toronto.neighbourhoods
        points = []
        for subregion in hoods:
            data['Cases'].append(hoods[subregion].scaled_case_index)
            data['Income'].append(hoods[subregion].scaled_economic_index)
            if hoods[subregion].scaled_case_index != 0 and hoods[subregion].scaled_economic_index != 0:
                points.append((hoods[subregion].scaled_economic_index, hoods[subregion].scaled_case_index))
        regression_model = ExponentialRegressionModel(points, 1000)

        df = pd.DataFrame(data)
        ax = df.plot.scatter(x='Income', y='Cases')
        a, b = 5.2327, 0.7709
        x = np.linspace(0, 10, 100)
        y = (regression_model.b**x) * regression_model.a
        plt.plot(x, y)
        plt.scatter(data['Income'], data['Cases'])
        plt.show()

    def toronto_region_heatmap(self) -> None:
        """ Creates a heat map of a region """
        sns.set(style='whitegrid', palette='pastel', color_codes=True)
        sns.mpl.rc('figure', figsize=(10, 6))

        shp_path = 'hood_shps/Neighbourhoods.shp'

        sf = shp.Reader(shp_path)
        plt.figure(figsize=(11, 9))
        id = 0
        for p in range(len(sf.shapeRecords())):
            shape = sf.shapeRecords()[p]
            name = sf.records()[p][7]
            name_result = ''
            name_list = name.split()
            for word in range(len(name_list)-1):
                name_result += (" " + name_list[word])
            name_result.rstrip()
            colours = ['#dadaebFF', '#bcbddcF0', '#9e9ac8F0',
             '#807dbaF0', '#6a51a3F0', '#54278fF0']
            colour = ''
            toronto = self.system.regions['Toronto']
            num_cases = toronto.neighbourhoods['name_result'].num_cases_per_cap
            print(name_result)
            x = [i[0] for i in shape.shape.points[:]]
            y = [i[1] for i in shape.shape.points[:]]

            plt.plot(x, y, 'k')
            plt.fill(x, y, 'r')
            x0 = np.mean(x)
            y0 = np.mean(y)

            plt.text(x0, y0, name_result, fontsize=5)
            id = id + 1


def draw_visuals_toronto():
    p = PreprocessingSystem()
    p.init_toronto_model()
    r = RegionVisual(p)
    r.toronto_scatter_visual()


def draw_heat_toronto():
    p = PreprocessingSystem()
    r = RegionVisual(p)
    r.toronto_region_heatmap()
