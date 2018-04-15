# -*- coding: utf-8 -*-
"""
Created on Sun Apr 15 17:30:00 2018

@author: artem
"""

import csv
from collections import defaultdict

from sklearn.cluster import KMeans

def kmeans(path=None, n_clusters=3):
    if path is None:
        return
    random_state = 170
    FILENAME = path
    X, y = [], []
    with open(FILENAME, 'r', newline='') as file:
        reader = csv.reader(file)
        reader.__next__()
        for row in reader:
            X.append(list(map(float, row[:-1])))
            y.append(row[-1])
    
    kmeans = KMeans(n_clusters=n_clusters, random_state=random_state).fit(X)
    cluster_centers = kmeans.cluster_centers_
    y_pred = kmeans.predict(X)
    
    cluster_centers = list(map(list, cluster_centers))
    for i in range(n_clusters):
        cluster_centers[i] = list(map(lambda x: round(x, 2), 
                       cluster_centers[i]))
    
    indexes = [[] for i in range(n_clusters)]
    for i in range(len(y_pred)):
        for clst in range(n_clusters):
            if y_pred[i] == clst:
                indexes[clst].append(i)
    
    classes_in_clusters = list(indexes)
    count_cic = [defaultdict(int) for i in range(n_clusters)]
    for clst in range(n_clusters):
        for j in range(len(classes_in_clusters[clst])):
            classes_in_clusters[clst][j] = y[indexes[clst][j]]
        for cls in set(classes_in_clusters[clst]):
            count_cic[clst][cls] = classes_in_clusters[clst].count(cls)
        count_cic[clst] = dict(count_cic[clst])
        for cls in count_cic[clst].keys():
            if count_cic[clst][cls] == max(count_cic[clst].values()):
                cluster_centers[clst].append(cls)     
    
    FILENAME = path.replace('csvs/', '')
    with open(FILENAME, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerows(cluster_centers)