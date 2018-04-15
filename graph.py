# -*- coding: utf-8 -*-
"""
Created on Thu Apr 5 22:40:00 2018

@author: artem
"""

import numpy as np
import matplotlib.pyplot as plt
import os

def graph (path=None, algorithms=None, dataname=None):
    if path is None or algorithms is None or dataname is None:
        return
    if path[-1] != '/':
        path = path + '/'
    results = []
    file_path = path.split('/')
    file_path.extend(['', ''])
    for algorithm in algorithms:
        algorithm_results = []
        path[-2] = algorithm
        path[-1] = algorithm + dataname + '.txt'
        file = open('/'.join(file_path), 'r')
        for line in file:
            algorithm_results.append(list(map(float, line.replace(',', '.')\
                                              .replace('\n', '').split(' '))))
        file.close()
        new_file_path = path.insert(-1, 'USED')
        os.rename('/'.join(file_path), '/'.join(new_file_path))
        algorithm_results = np.array(algorithm_results)
        algorithm_results = np.mean(algorithm_results, axis=0)
        results.append(algorithm_results)
    
    for algorithm_results in results:
        plt.plot(range(len(algorithm_results)), algorithm_results)
    plt.title(dataname)
    plt.xlabel('Итерации')
    plt.ylabel('Точность, %')
    plt.legend(algorithms)
    plt.savefig(path + 'images/' + '_'.join(algorithms) + '_' + dataname + 
                '.png', format='png')
    plt.show()