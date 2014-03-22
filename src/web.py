import json
import random

from flask import Flask, render_template, jsonify
app = Flask(__name__)

import pandas as pd
import numpy as np

import config

df = pd.read_pickle(config.db_df_pickle)
cluster_data = pd.read_pickle(config.cluster_df_pickle)
cluster_types = np.unique(tag for hashtags in cluster_data['types'].values for tag in hashtags)
cluster_types = filter(lambda type : len(cluster_data[cluster_data['types'].map(lambda types: type in types)]) > 5, cluster_types)

@app.route("/")
def index():
    return render_template('index.html', cluster_types=cluster_types)

@app.route('/api/clusters')
def get_clusters():
    clusters = json.loads(cluster_data.to_json(orient='records'))
    return jsonify(ok=True, clusters=clusters)

@app.route('/api/clusters/<cluster_type>')
def get_clusters_by_type(cluster_type):
    clusters = json.loads(cluster_data[cluster_data['types'].map(lambda t: cluster_type in t)].to_json(orient='records'))
    return jsonify(ok=True, clusters=clusters)

@app.route("/api/clusters/<int:cluster>/pictures")
def get_pictures_by_cluster(cluster):
    center = cluster_data.ix[cluster].center
    pictures = df[df['cluster'] == cluster]

    # Limiting number of results
    pictures = pictures.ix[random.sample(pictures.index, min(len(pictures), 100))]

    rows = json.loads(pictures.to_json(orient='records'))
    return jsonify(ok=True, pictures=rows, center=center)


if __name__ == "__main__":
    app.run(debug=True)
