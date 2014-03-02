#!/usr/bin/env python
# -*- coding: utf-8 -*-
import pandas as pd
import numpy as np
import pylab as pl
from mpl_toolkits.mplot3d import Axes3D
from sklearn.cluster import KMeans
from sklearn import datasets

import config

# Parsing raw CSV file
db = pd.read_csv(config.db_path)
# Splitting the hashtag to lists
db['hashtags'] = db['hashtags'].apply(lambda hashtags : str(hashtags).split(','))

centers = [[1, 1], [-1, -1], [1, -1]]
iris = datasets.load_iris()

X = db.filter(['latitude', 'longitude', 'hour_taken']).values[:100]
y = db['row ID'].values[:100]

print iris.data[:10]
print X[:10]

estimators = {'k_means_4': KMeans(n_clusters=4),
              'k_means_8': KMeans(n_clusters=8)}

for fignum, (name, estimator) in enumerate(estimators.iteritems()):
    fig = pl.figure(fignum, figsize=(4, 3))
    pl.clf()
    ax = Axes3D(fig, rect=[0, 0, .95, 1], elev=48, azim=134)

    pl.cla()
    estimator.fit(X)
    labels = estimator.labels_

    ax.scatter(X[:, 0], X[:, 1], X[:, 2], c=labels.astype(np.float))

    ax.w_xaxis.set_ticklabels([])
    ax.w_yaxis.set_ticklabels([])
    ax.w_zaxis.set_ticklabels([])

    ax.set_xlabel('Latitude')
    ax.set_ylabel('Longitude')
    ax.set_zlabel('Hour taken')

# Plot the ground truth
fig = pl.figure(fignum, figsize=(4, 3))
pl.clf()
ax = Axes3D(fig, rect=[0, 0, .95, 1], elev=48, azim=134)

pl.cla()
pl.show()
