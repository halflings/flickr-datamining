import json
from flask import Flask, render_template, jsonify
app = Flask(__name__)

from mining import df, ms

@app.route("/")
def index():
    return render_template('index.html')

@app.route("/api/points")
def get_data():
    rows = json.loads(df[:1000].to_json(orient='records'))
    return jsonify(ok=True, points=rows)


@app.route("/api/points/<int:cluster>")
def get_data_by_cluster(cluster):
    center = ms.cluster_centers_[cluster].tolist()
    rows = json.loads(df[df['cluster'] == cluster][:1000].to_json(orient='records'))
    return jsonify(ok=True, points=rows, center=center)


if __name__ == "__main__":
    app.run(debug=True)
