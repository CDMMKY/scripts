# -*- coding: utf-8 -*-
"""
Created on Sun Apr 15 17:30:00 2018

@author: artem
"""

import csv


def export_dat_to_csv(path=None):
    if path is None:
        return
    else:
        f = open(path, 'r')
    columns = []
    rows = []
    for line in f:
        if '@inputs' in line:
            new_line = line.replace('@inputs ', '').replace('\n', '')
            columns = new_line.split(', ')
            columns.append('Class')
        if '@' not in line:
            row = line.split(', ')
            row[:-1] = list(map(float, row[:-1]))
            row[-1] = row[-1].replace('\n', '')
            rows.append(row)
    f.close()
    
    FILENAME = path.replace('dats', 'csvs').replace('dat', 'csv')
    with open(FILENAME, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(columns)
        writer.writerows(rows)
