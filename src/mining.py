#!/usr/bin/env python
# -*- coding: utf-8 -*-
import random
import pandas as pd
import numpy as np
import pylab as pl
from itertools import cycle
from sklearn.cluster import MeanShift, estimate_bandwidth

import places
import config

#################################################################################
# Loading data
def read_data(path):
    columns = [
        'id', 'user', 'longitude', 'latitude', 'hashtags', 'legend',
        'minutes_taken', 'hour_taken', 'day_taken', 'month_taken', 'year_taken', 'url'
    ]

    df = pd.read_csv(path, usecols=columns, sep=',', encoding='latin-1')

    df = df[
        (df.minutes_taken >= 0) & (df.minutes_taken < 60) &
        (df.hour_taken >= 0) & (df.hour_taken < 24) &
        (df.day_taken >= 0) & (df.day_taken < 31) &
        (df.month_taken >= 0) & (df.month_taken < 12) &
        (df.year_taken >= 2000) & (df.year_taken <= 2014) &
        (45.5 < df.latitude) & (df.latitude < 46.0) &
        (4.4 < df.longitude) & (df.longitude < 5.2)
    ]

    columns_float = ['latitude', 'longitude']
    columns_int = ['id', 'minutes_taken', 'hour_taken', 'day_taken', 'month_taken', 'year_taken']
    columns_na = []
    columns_na.extend(columns_float)
    columns_na.extend(columns_int)

    df[columns_float] = df[columns_float].astype(float)

    df[columns_int] = df[columns_int].astype(int)

    df = df.dropna(subset=columns_na)
    df[['hashtags', 'legend']] = df[['hashtags', 'legend']].fillna(value='')

    grouped = df.groupby(columns)
    index = [gp_keys[0] for gp_keys in grouped.groups.values()]
    df = df.reindex(index)

    # Adding some fake entropy to latitude
    df['latitude'] = df['latitude'].apply(lambda latitude : latitude - 0.0005 + (random.randint(0, 9) / 10000.0))
    # Tokenizing hashtags
    df['hashtags'] = df['hashtags'].apply(lambda tags : tags.split(',') if tags else [])
    # Cleaning legend's HTML
    df['legend'] = df['legend'].apply(lambda legend : legend.replace('\\n', '<br>'))
    # Replacing small images by medium sized images
    df['url'] = df['url'].apply(lambda url : url.replace('_t.jpg', '_m.jpg'))

    return df

df = read_data(config.db_path)

#################################################################################
# Clustering
X = df[['latitude', 'longitude']].values
bandwidth = estimate_bandwidth(X, quantile=0.0005, n_samples=10000)

clustering = MeanShift(bandwidth=bandwidth, bin_seeding=True, cluster_all=False, min_bin_freq=10)
clustering.fit(X)
labels = clustering.labels_
df['cluster'] = clustering.labels_
cluster_centers = clustering.cluster_centers_

labels_unique = np.unique(l for l in labels if l != -1)
n_clusters_ = len(labels_unique)

cluster_count = df[df['cluster'] != -1].groupby('cluster').size()

# Building a DataFrame describing each cluster
c_data = list()
for cluster in labels_unique:
    center = clustering.cluster_centers_[cluster].tolist()
    data = dict(cluster=cluster, count=cluster_count[cluster], center=center)
    print cluster, center

    # Including data from the Google Places API
    places_data_list = places.nearby_places(round(center[0], 4), round(center[1], 4))
    if places_data_list:
        places_with_photo = [p for p in places_data_list if 'main_photo' in p]
        places_data = places_with_photo[0] if places_with_photo else places_data_list[0]
        data['name'] = places_data['name']
        data['rating'] = places_data.get('rating', None)
        data['types'] = places_data['types']
        data['vicinity'] = places_data['vicinity']
        data['photo'] = places_data.get('main_photo')
        data['icon'] = places_data['icon']
        print data['vicinity'], data['photo']


    c_data.append(data)

cluster_data = pd.DataFrame(c_data)
cluster_data.set_index('cluster')

# Saving the dataframes to pickle files
df.to_pickle(config.db_df_pickle)
cluster_data.to_pickle(config.cluster_df_pickle)

if __name__ == '__main__':
    ###############################################################################
    # Plot result
    pl.figure(1)
    pl.clf()

    colors = cycle('bgrcmykbgrcmykbgrcmykbgrcmyk')
    for k, col in zip(range(n_clusters_), colors):
        if k == -1:
            continue

        my_members = labels == k
        cluster_center = cluster_centers[k]
        pl.plot(X[my_members, 0], X[my_members, 1], col + '.')
        pl.plot(cluster_center[0], cluster_center[1], 'o', markerfacecolor=col,
                markeredgecolor='k', markersize=14)
    pl.title('Estimated number of clusters: %d' % n_clusters_)
    pl.show()
