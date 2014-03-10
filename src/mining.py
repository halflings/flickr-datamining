import pandas as pd
import numpy as np
import pylab as pl
from itertools import cycle
from sklearn.cluster import MeanShift, estimate_bandwidth

import config

#################################################################################
# Loading data
def read_data(path):
    columns = [
        'id', 'user', 'longitude', 'latitude', 'hashtags', 'legend',
        'minutes_taken', 'hour_taken', 'day_taken', 'month_taken', 'year_taken'
    ]

    df = pd.read_csv(path, encoding='latin-1', usecols=columns, sep='\t')

    df = df[
        (df.minutes_taken >= 0) & (df.minutes_taken < 60) &
        (df.hour_taken >= 0) & (df.hour_taken < 24) &
        (df.day_taken >= 0) & (df.day_taken < 31) &
        (df.month_taken >= 0) & (df.month_taken < 12) &
        (df.year_taken >= 2000) & (df.year_taken <= 2014)
    ]

    columns_float = ['latitude', 'longitude']
    columns_int = ['id', 'minutes_taken', 'hour_taken', 'day_taken', 'month_taken', 'year_taken']
    columns_na = []
    columns_na.extend(columns_float)
    columns_na.extend(columns_int)

    df[columns_float] = df[columns_float].astype(float)
    df[columns_int] = df[columns_int].astype(int)

    df = df.dropna(subset=columns_na)

    grouped = df.groupby(columns)
    index = [gp_keys[0] for gp_keys in grouped.groups.values()]
    df = df.reindex(index)

    return df

df = read_data("../sujet/flickr.csv")

#################################################################################
# latitude and longitude
X = df[['latitude', 'longitude']].values

#################################################################################
# Clustering
bandwidth = estimate_bandwidth(X, quantile=0.002, n_samples=1000)

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
