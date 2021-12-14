"""
Module Name: Data Collection Module
Source Path: modules/data_collection.py

Description:

This module opens and reads all 140 neighbourhood profile pdfs from the Toronto Neighbourhood
Profiles website, and attains the name, population and median household income. Some neighbourhood
names require a rather robust method of data filtration, as the names on the pdf files do not
perfectly correlate to the names on the covid data csv files.

===============================

CSC110 Final Project:

"Virus of Inequality: The Socio-Economic Disparity of COVID-19 Cases
in the City of Toronto"

This file is Copyright (c) 2021 Harvey Ronan Donnelly and Ewan Robert Jordan.
"""
import tabula as tb
import requests
import io
from string import digits
import csv


def scrape_incomes() -> None:
    """ Attains population, name and median household income from Toronto neighbourhood profile pdfs"""
    info = [('Region', 'Population', 'Median Household Income(pre-tax)'), ('Toronto', 2731571, 65829)]
    for i in range(1, 141):
        file_num = str(i)
        if i < 10:
            file_num = "0" + str(i)
        urlpdf = "https://www.toronto.ca/ext/sdfa/Neighbourhood%20Profiles/pdf/2016/pdf1/cpa" + file_num + ".pdf"
        response = requests.get(urlpdf)
        with io.BytesIO(response.content) as f:
            data = tb.read_pdf(urlpdf, area=(400, 300, 500, 800), pages='3')
            income = int(''.join(filter(str.isdigit, str(data[0]['Neighbourhood'][0]))))

            name = tb.read_pdf(urlpdf, area=(0, 0, 50, 800), pages='3')
            name_str = name[0].columns[-1]
            name_fin = name_str.translate(digits)[3:]
            if name_fin[0] == '.':
                namep = name_fin[1:]
            else:
                namep = name_fin
            name_final = namep.strip()
            print(name_final)
#  these conditionals are here to fix minor spelling differences between these neighbourhood names
#  and those of the covid case data
            if name_final[0:5] == 'Briar':
                name_final = 'Briar Hill - Belgravia'
            elif name_final == 'Danforth East York':
                name_final = 'Danforth-East York'
            elif name_final == 'Weston-Pelham Park':
                name_final = 'Weston-Pellam Park'

            population = tb.read_pdf(urlpdf, area=(100, 0, 200, 250), pages='3')
            pop = int(''.join(filter(str.isdigit, str(population[0]['Neighbourhood'][0]))))
            info.append((name_final, pop, income))
    with open('../data/test_toronto_regions.csv', 'w', newline='') as out:
        csv_out = csv.writer(out)
        for row in info:
            csv_out.writerow(row)
            print('r')


scrape_incomes()
