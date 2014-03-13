import json
import random

from flask import Flask, render_template, jsonify
app = Flask(__name__)

import pandas as pd

import config

df = pd.read_pickle(config.db_df_pickle)
cluster_data = pd.read_pickle(config.cluster_df_pickle)

@app.route("/")
def index():
    return render_template('index.html')

@app.route('/api/clusters')
def get_clusters():
    clusters = json.loads(cluster_data.to_json(orient='records'))
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
