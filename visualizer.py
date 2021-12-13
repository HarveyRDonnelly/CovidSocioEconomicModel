""" Visualizes covid data for a given system """
from preprocessing import PreprocessingSystem
from regression import ExponentialRegressionModel
import pandas as pd
import numpy as np
import shapefile as shp
import matplotlib.pyplot as plt
import seaborn as sns


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

    def toronto_heatmap(self, variable: str) -> None:
        """ Creates a heat map of a region's covid numbers """
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
            name_result = name_result.strip()
            name_result = self.neighbourhood_name_filtration(name_result)
            x = [i[0] for i in shape.shape.points[:]]
            y = [i[1] for i in shape.shape.points[:]]
            colour = self.get_colour(name_result, variable)
            plt.plot(x, y, 'k')
            plt.fill(x, y, colour)
            x0 = np.mean(x)
            y0 = np.mean(y)
            id = id + 1

    def get_colour(self, name_result: str, variable: str) -> str:
        """ Returns the colour corresponding to the amount of covid cases
            per capita in a neighbourhood"""
        colour = ''
        if variable == 'Covid':
            colours = ['#dadaebFF', '#bcbddcF0', '#9e9ac8F0',
                       '#807dbaF0', '#6a51a3F0', '#54278fF0']
            toronto = self.system.regions['Toronto']
            num_cases = toronto.neighbourhoods[name_result].num_cases_per_cap
            if num_cases < 1000:
                colour = colours[0]
            elif 1000 <= num_cases < 1800:
                colour = colours[1]
            elif 1800 <= num_cases < 2600:
                colour = colours[2]
            elif 2600 <= num_cases < 3400:
                colour = colours[3]
            elif 3400 <= num_cases < 4200:
                colour = colours[4]
            elif num_cases >= 4200:
                colour = colours[5]
            return colour
        elif variable == 'Income':
            colours = ['#ffffd4', '#fee391', '#fec44f',
                       '#fe9929', '#d95f0e', '#993404']
            toronto = self.system.regions['Toronto']
            income = toronto.neighbourhoods[name_result].median_household_income
            if income < 50000:
                colour = colours[5]
            elif 50000 <= income < 70000:
                colour = colours[4]
            elif 70000 <= income < 90000:
                colour = colours[3]
            elif 90000 <= income < 110000:
                colour = colours[2]
            elif 110000 <= income < 150000:
                colour = colours[1]
            elif income >= 150000:
                colour = colours[0]
            return colour

    def neighbourhood_name_filtration(self, name_result: str) -> str:
        """ Returns neighbourhood names which match up with other datasets"""
        if name_result == 'North St.James Town':
            name_result = 'North St. James Town'
        if name_result == 'Danforth East York':
            name_result = 'Danforth-East York'
        if name_result == 'Briar Hill-Belgravia':
            name_result = 'Briar Hill - Belgravia'
        if name_result == 'Cabbagetown-South St.James Town':
            name_result = 'Cabbagetown-South St. James Town'
        return name_result


def draw_visuals_toronto():

    p = PreprocessingSystem()
    p.init_toronto_model()
    r = RegionVisual(p)
    r.toronto_scatter_visual()


def draw_heat_toronto():
    p = PreprocessingSystem()
    p.init_toronto_model()
    r = RegionVisual(p)
    r.toronto_heatmap('Covid')
    r.toronto_heatmap('Income')

draw_heat_toronto()
