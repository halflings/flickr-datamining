import pandas as pd
import numpy as np
import pylab as pl
from itertools import cycle
from sklearn.cluster import MeanShift, estimate_bandwidth
import places

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
    # Tokenizing hashtags
    df['hashtags'] = df['hashtags'].apply(lambda tags : tags.split(',') if tags else [])
    # Cleaning legend's HTML
    df['legend'] = df['legend'].apply(lambda legend : legend.replace('\\n', '<br>'))
    # Replacing small images by medium sized images
    df['url'] = df['url'].apply(lambda url : url.replace('_t.jpg', '_m.jpg'))

    return df

df = read_data("../sujet/flickr.csv")

#################################################################################
# Clustering
X = df[['latitude', 'longitude']].values
bandwidth = estimate_bandwidth(X, quantile=0.0005, n_samples=10000)

clustering = MeanShift(bandwidth=bandwidth, bin_seeding=True, cluster_all=False, min_bin_freq=10)
clustering.fit(X)
labels = clustering.labels_
df['cluster'] = clustering.labels_
cluster_centers = clustering.cluster_centers_

labels_unique = np.unique(labels)
n_clusters_ = len(labels_unique)

cluster_data = df[df['cluster'] != -1].groupby('cluster').size()
# cluster_data['center'] = cluster_data['cluster'].apply(lambda c : clustering.cluster_centers_[c])

################################################################################
# Adding data from Google Places API
# rating -> 4
# name -> La Fontaine
# reference -> CnRsAAAARvBHQbC4mhuh_IHzFmMbE_NmBcVbF0yaJ6bE4eDkUtsWy0G9F7TVQP2f5w31IhRW9jTIrkWhZ_UJCEH8c0Xl_PAW1eogWaRn6TGeutsd0sHKPD6AcYrS6HjCns1QT_-blaHSD2pfYD3oB1CgtJ8IDhIQ5hvKFsOg21FG2S7DOM7BxhoU5T_cVdCRX4yJTki7wVw8GugurKE
# geometry -> {u'location': {u'lat': 45.767812, u'lng': 4.833419}}
# vicinity -> 7 Place des Terreaux, Lyon
# photos -> [{u'photo_reference': u'CqQBkwAAACGUQhphaUgN0Z7oDHl0TBqDyYQOVmV3-ibSmiLa89wSFHLy5fTnwBbX4rL4gVUm7Ew33OzpIu1qA23FVnGCHYwTcnvtHZJVaMv1tqIuD0z68ouN_Al6KzjNJgGvFrJ9ySyIseno4ZgIL97I8mEQLqoJcwWrUact3iTA8s1vaHMHNokbL_gG1UIotUfqiPofJ3xTyefyHNU-4-WG0kXUULMSEB6gFFUBJNJupHt3-men4NQaFAnGAX1uLVvYSvaYaTNmEkek6dYd', u'width': 2048, u'html_attributions': [u'From a Google User'], u'height': 1536}]
# id -> 947d275c257491d288e7b5156a00359285d754fb
# types -> [u'restaurant', u'food', u'establishment']
# icon -> http://maps.gstatic.com/mapfiles/place_api/icons/restaurant-71.png

# df[] = df1['e'] = df1['a'].map(lambda x: np.random.random())


###############################################################################
# Plot result

if __name__ == '__main__':
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
