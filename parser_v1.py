# -*- coding: utf-8 -*-
"""
Created on Tue Mar 20 15:00:00 2018

@author: artem
"""

import os


def parse_folder(path=None, n_populations=10, mode='bagging', ext='.txt'):
    if path is None:
        return
    list_files = filter(lambda x: x.endswith(ext), os.listdir(path))
    path = path.split('/')
    path.append('')
    for file in list_files:
        path[-1] = file
        parse_file('/'.join(path), mode, n_populations)


def parse_file(path=None, mode='bagging', n_populations=10):
    if path is None:
        return
    
    data = read_data_from_file(path)
    
    if mode == 'bagging':        
        data = extract_bagging(data, n_populations)
    
    results = []
    for elem in data:
        results.append(average(elem))
    
    print_results(results, mode)
    write_results(path, results, mode)
    
    move_file_to_used(path)


def read_data_from_file(path=None):
    learn, test = [], []
    f = open(path, 'r')
    for line in f:
        new_line = line.replace('\n', '')
        new_line = new_line.replace(',', '.')
        if "Обуч: " in new_line:
            learn.append(float(new_line.replace("Обуч: ", '')))
        elif "Тест: " in new_line:
            test.append(float(new_line.replace("Тест: ", '')))
    f.close()
    return (learn, test)


def extract_bagging(data, n_populations):
    learnbag, testbag = [], []
    for i in range(len(data[0])-1, n_populations-1, -(n_populations+1)):
            learnbag.append(data[0].pop(i))
            testbag.append(data[1].pop(i))
    return (data[0], data[1], learnbag, testbag)


def print_results(results, mode):
    print('Среднее:\t{0}\t{1}'.format(results[0], results[1]))
    if mode == 'bagging':
        print('Баггинг:\t{0}\t{1}'.format(results[2], results[3]))


def write_results(path, results, mode):
    path_to_results = path.split('/')
    dataset_name = path_to_results[-1]
    path_to_results[-1] = 'Результаты'
    path_to_results.append('results.txt')
    f = open('/'.join(path_to_results), 'a')
    f.write('{0}\nСреднее: {1} {2}\n'.format(dataset_name[:-4], results[0],
            results[1]))
    if mode == 'bagging':
        f.write('Баггинг: {1} {2}\n'.format(results[2], results[3]))
    f.close()


def move_file_to_used(path):
    path_to_used = path.split('/')
    path_to_used.insert(-1, 'USED')
    os.rename(path, '/'.join(path_to_used))


def average(struct):
    return round(sum(struct)/len(struct), 2)