import json
import random

from flask import Flask, render_template, jsonify
app = Flask(__name__)

from mining import df, clustering

cluster_data = df.groupby('cluster').size()

@app.route("/")
def index():
    return render_template('index.html')

@app.route('/api/clusters')
def get_clusters():
    data = [dict(cluster=c, center=clustering.cluster_centers_[c].tolist(), count=count)
            for c, count in enumerate(cluster_data.values)]
    return jsonify(ok=True, clusters=data)

@app.route("/api/pictures")
def get_pictures():
    # Limiting number of results
    pictures = df.ix[random.sample(df.index, min(len(df), 1000))]

    rows = json.loads(pictures.to_json(orient='records'))
    return jsonify(ok=True, pictures=rows)

@app.route("/api/clusters/<int:cluster>/pictures")
def get_pictures_by_cluster(cluster):
    center = clustering.cluster_centers_[cluster].tolist()
    pictures = df[df['cluster'] == cluster]

    # Limiting number of results
    pictures = pictures.ix[random.sample(pictures.index, min(len(pictures), 100))]

    rows = json.loads(pictures.to_json(orient='records'))
    return jsonify(ok=True, pictures=rows, center=center)


if __name__ == "__main__":
    app.run(debug=True)
