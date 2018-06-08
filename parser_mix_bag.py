# -*- coding: utf-8 -*-
"""
Created on Sun Apr 15 17:33:00 2018

@author: artem
"""

import os


def parse_folder(path=None, n_populations=[10, 10], n_algorithms=2,
                 mode='bagging', ext='.txt'):
    if path is None:
        return
    list_files = filter(lambda x: x.endswith(ext), os.listdir(path))
    path = path.split('/')
    path.append('')
    for file in list_files:
        path[-1] = file
        parse_file('/'.join(path), n_populations=n_populations)


def parse_file(path=None,  n_populations=[10,10], n_algorithms=2, 
               mode='bagging'):
    if path is None:
        return
    
    data_from_file = read_data_from_file(path)
    
    parsed_data = parse_data(data_from_file, mode, n_populations, n_algorithms)
            
    print_results(parsed_data, mode, n_populations, n_algorithms)


def read_data_from_file(path=None):
    data_from_file = []
    f = open(path, 'r')
    for line in f:
        new_line = line.replace('\n', '')
        new_line = new_line.replace(',', '.')
        if "Обуч: " in new_line:
            data_from_file.append(float(new_line.replace("Обуч: ", '')))
        elif "Тест: " in new_line:
            data_from_file.append(float(new_line.replace("Тест: ", '')))
    f.close()
    return data_from_file


def parse_data(data_from_file, mode, n_populations, n_algorithms):
    learn = [[] for i in range(n_algorithms)]
    test = [[] for i in range(n_algorithms)]
    learn_bagging = [[] for i in range(n_algorithms)]
    test_bagging = [[] for i in range(n_algorithms)]
    learn_mixbagging = []
    test_mixbagging = []
    while len(data_from_file) > 0:
        for i in range(n_algorithms):
            for j in range(n_populations[i]):
                learn[i].append(data_from_file.pop(0))
                test[i].append(data_from_file.pop(0))
        if mode == 'bagging':
            for i in range(n_algorithms):
                learn_bagging[i].append(data_from_file.pop(0))
                test_bagging[i].append(data_from_file.pop(0))
        if mode == 'bagging' and n_algorithms > 1:
            learn_mixbagging.append(data_from_file.pop(0))
            test_mixbagging.append(data_from_file.pop(0))
    return (learn, test, learn_bagging, test_bagging, learn_mixbagging,
            test_mixbagging)
    

def print_results(data, mode, n_populations, n_algorithms):
    for i in range(n_algorithms):
        print('Среднее:\t{0}\t{1}'.format(average(data[0][i]), 
              average(data[1][i])))
        if mode == 'bagging':
            print('Баггинг:\t{0}\t{1}'.format(average(data[2][i]), 
                  average(data[3][i])))
    if mode == 'bagging' and n_algorithms > 1:
        print('Mix Bagging:\t{0}\t{1}'.format(average(data[4]), 
              average(data[5])))


def average(struct):
    return round(sum(struct)/len(struct), 2)
