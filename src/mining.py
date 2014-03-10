import pandas as pd
import numpy as np
import pylab as pl
from itertools import cycle
from sklearn.cluster import MeanShift, estimate_bandwidth

import config

#################################################################################
# Loading data
df = pd.read_csv(config.db_path, encoding='latin-1')
X = df[['latitude', 'longitude']].values

#################################################################################
# Clustering
bandwidth = estimate_bandwidth(X, quantile=0.05, n_samples=1000)

clustering = MeanShift(bandwidth=bandwidth, bin_seeding=True)
clustering.fit(X)
labels = clustering.labels_
df['cluster'] = clustering.labels_
cluster_centers = clustering.cluster_centers_

labels_unique = np.unique(labels)
n_clusters_ = len(labels_unique)

###############################################################################
# Plot result

if __name__ == '__main__':
    pl.figure(1)
    pl.clf()

    colors = cycle('bgrcmykbgrcmykbgrcmykbgrcmyk')
    for k, col in zip(range(n_clusters_), colors):
        my_members = labels == k
        cluster_center = cluster_centers[k]
        pl.plot(X[my_members, 0], X[my_members, 1], col + '.')
        pl.plot(cluster_center[0], cluster_center[1], 'o', markerfacecolor=col,
                markeredgecolor='k', markersize=14)
    pl.title('Estimated number of clusters: %d' % n_clusters_)
    pl.show()
