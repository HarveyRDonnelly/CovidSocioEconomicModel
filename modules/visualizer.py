"""
Module Title: Model Visualizer
Source Path: modules/visualizer.py

Description:

This module holds a class for creating visuals for a preprocessing system. It is able to create 4
different graphics, two toronto heat maps, one showing the difference in income in the toronto
region, and the other showing the covid case intensity in the toronto region, and two scatter plots,
both showing the correlation between scaled economic index and scaled case index. One however shows
the logarithm of the points to create a linear regression, while the other shows the actual points
along with an exponential line of best fit.

===============================

CSC110 Final Project:

"Virus of Inequality: The Socio-Economic Disparity of COVID-19 Cases
in the City of Toronto"

This file is Copyright (c) 2021 Harvey Ronan Donnelly and Ewan Robert Jordan.
"""
from modules.preprocessing import PreprocessingSystem
from modules.regression import ExponentialRegressionModel
from modules.config import TorontoConfig

import numpy as np
import shapefile as shp
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import seaborn as sns

config = TorontoConfig()


class RegionVisual:
    """
    Creates a shapely visual of different attributes of a region

    Instance Attributes:
    - system: the preprocessing system which will have visuals created for.
    """
    system: PreprocessingSystem

    def __init__(self, system: PreprocessingSystem):
        self.system = system
        self.colours_covid = ['#dadaebFF', '#bcbddcF0', '#9e9ac8F0',
                              '#807dbaF0', '#6a51a3F0', '#54278fF0']
        self.colours_income = ['#993404', '#d95f0e',
                               '#fe9929', '#fec44f', '#fee391', '#ffffd4']

        self.ranges_covid = ['less than 3000', '3000 to 3800', '3800 to 4600',
                             '4600 to 6400', '6400 to 9200', 'more than 9200']

        self.ranges_income = ['less than 50,000 CAD', '50,000 CAD to 70,000 CAD',
                              '70,000 CAD to 90,000 CAD', '90,000 CAD ' + 'to ' + '110,000 CAD',
                              '110,000 CAD to 150,000 CAD', 'more than 150,000 CAD']

    def toronto_scatter_visual(self) -> None:
        """
        Creates a scatter plot comparing toronto neighbourhoods' income against covid cases.
        """
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
        x = np.linspace(0, 10, 100)
        y = (regression_model.b ** x) * regression_model.a
        fig, (ax1, ax2) = plt.subplots(1, 2)
        fig.suptitle('Visualizing the regression model: (September 2020 - December 2021)', fontweight="bold")
        ax1.plot(x, y)
        ax1.scatter(data['Income'], data['Cases'])
        ax1.set_title('Scaled Economic Index vs Scaled Case Index')
        ax1.set_xlabel("Scaled Economic Index", fontweight="bold")
        ax1.set_ylabel("Scaled Case Index", fontweight="bold")

        x = np.linspace(0, 10, 100)
        y = (regression_model.gradient * x) + regression_model.y_intercept
        ax2.plot(x, y)
        x_logs = []
        y_logs = []
        for point in regression_model.calculate_log_coordinates(points):
            x_logs.append(point[0])
            y_logs.append(point[1])
        ax2.scatter(x_logs, y_logs)
        ax2.set_title('Logarithm of Scaled Case Index vs Scaled Economic Index')
        ax2.set_xlabel("Scaled Economic Index", fontweight="bold")
        ax2.set_ylabel("ln(Scaled Case Index)", fontweight="bold")

    def toronto_heatmap(self, variable: str) -> None:
        """ Creates a heat map of a region's covid numbers.
            Preconditions:
            - variable in ['Covid', 'Income']
        """
        sns.set(style='whitegrid', palette='pastel', color_codes=True)
        sns.mpl.rc('figure', figsize=(10, 6))

        shp_path = config.paths['shapes']

        sf = shp.Reader(shp_path)
        plt.figure(figsize=(11, 9))
        id = 0
        for p in range(len(sf.shapeRecords())):
            shape = sf.shapeRecords()[p]
            name = sf.records()[p][7]
            name_result = ''
            name_list = name.split()
            for word in range(len(name_list) - 1):
                name_result += (" " + name_list[word])
            name_result = name_result.strip()
            name_result = self.neighbourhood_name_filtration(name_result)
            x = [i[0] for i in shape.shape.points[:]]
            y = [i[1] for i in shape.shape.points[:]]
            colour = self.get_colour(name_result, variable)
            plt.plot(x, y, 'k')
            plt.fill(x, y, colour)

            id = id + 1

        if variable == 'Covid':
            plt.title('Covid-19 Intensity in Toronto Neighbourhoods (cases per 100,000) '
                      '- (September 2020 - December 2021)')
            legend = [mpatches.Patch(color=col, label=rang) for col, rang in
                      zip(tuple(self.colours_covid), tuple(self.ranges_covid))]
            plt.legend(handles=legend)
        elif variable == 'Income':
            plt.title('Median Household Income in Toronto Neighbourhoods')
            legend = [mpatches.Patch(color=col, label=rang) for col, rang in
                      zip(tuple(self.colours_income), tuple(self.ranges_income))]
            plt.legend(handles=legend)
        plt.show()

    def get_colour(self, name_result: str, variable: str) -> str:
        """ Returns the colour corresponding to the amount of covid cases
            per capita in a neighbourhood.

            Preconditions:
            - name_result in toronto.neighbourhoods.keys()
            - variable in ['Covid', 'Income']
        """
        colour = ''
        if variable == 'Covid':
            colours = ['#dadaebFF', '#bcbddcF0', '#9e9ac8F0',
                       '#807dbaF0', '#6a51a3F0', '#54278fF0']
            toronto = self.system.regions['Toronto']
            num_cases = toronto.neighbourhoods[name_result].num_cases_per_cap
            if num_cases < 3000:
                colour = colours[0]
            elif 3000 <= num_cases < 3800:
                colour = colours[1]
            elif 3800 <= num_cases < 4600:
                colour = colours[2]
            elif 4600 <= num_cases < 6400:
                colour = colours[3]
            elif 6400 <= num_cases < 9200:
                colour = colours[4]
            elif num_cases >= 9200:
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
        """ Returns neighbourhood names which match up with other datasets.

            Preconditions:
            - len(name_result) > 0
        """
        if name_result == 'North St.James Town':
            name_result = 'North St. James Town'
        if name_result == 'Danforth East York':
            name_result = 'Danforth-East York'
        if name_result == 'Briar Hill-Belgravia':
            name_result = 'Briar Hill - Belgravia'
        if name_result == 'Cabbagetown-South St.James Town':
            name_result = 'Cabbagetown-South St. James Town'
        return name_result
