# -*- coding: utf-8 -*-
"""
Created on Sun Apr 15 17:33:00 2018

@author: artem
"""

import os

def average(struct):
    return round(sum(struct)/len(struct), 2)

def parse_file(folder=None, file=None,  n_populations=[10], n_algorithms=1,
               mode='bagging'):
    if file is None:
        return
    data_from_file = []
    learn = [[] for i in range(n_algorithms)]
    test = [[] for i in range(n_algorithms)]
    learnbag = [[] for i in range(n_algorithms)]
    testbag = [[] for i in range(n_algorithms)]
    mix_bagging_learn = []
    mix_bagging_test = []
    if folder is None:
        f = open('./' + file, 'r')
    else:
        f = open(folder + '/' + file, 'r')
    
    for line in f:
        new_line = line.replace('\n', '')
        new_line = new_line.replace(',', '.')
        if "Обуч: " in new_line:
            data_from_file.append(float(new_line.replace("Обуч: ", '')))
        elif "Тест: " in new_line:
            data_from_file.append(float(new_line.replace("Тест: ", '')))
    
    f.close()
    
    while len(data_from_file) > 0:
        for i in range(n_algorithms):
            for j in range(n_populations[i]):
                learn[i].append(data_from_file.pop(0))
                test[i].append(data_from_file.pop(0))
        if mode == 'bagging':
            for i in range(n_algorithms):
                learnbag[i].append(data_from_file.pop(0))
                testbag[i].append(data_from_file.pop(0))
        if mode == 'bagging' and n_algorithms > 1:
            mix_bagging_learn.append(data_from_file.pop(0))
            mix_bagging_test.append(data_from_file.pop(0))
            
    for i in range(len(n_populations)):
        print('Среднее:\t{0}\t{1}'.format(average(learn[i]), 
              average(test[i])))
        if mode == 'bagging':
            print('Баггинг:\t{0}\t{1}'.format(average(learnbag[i]), 
                  average(testbag[i])))
    if mode == 'bagging' and n_algorithms > 1:
        print('Mix Bagging:\t{0}\t{1}'.format(average(mix_bagging_learn), 
              average(mix_bagging_test)))
    
def parse_folder(folder=None, n_populations=[10, 10], n_algorithms=2,
                 mode='bagging', ext='.txt'):
    list_files = filter(lambda x: x.endswith(ext), os.listdir(folder))
    for file in list_files:
        parse_file(folder, file, n_populations, n_algorithms, mode)
        os.rename(folder + '/' + file, folder + '/OLD/' + file)
