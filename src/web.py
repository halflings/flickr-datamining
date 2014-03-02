import pandas as pd
from flask import Flask, render_template, jsonify
app = Flask(__name__)

import config

# Parsing raw CSV file
db = pd.read_csv(config.db_path)

@app.route("/")
def index():
    return render_template('index.html')

@app.route("/api/points")
def points():
    return jsonify(ok=True, points=db.filter(['latitude', 'longitude']).values[:200].tolist())

if __name__ == "__main__":
    app.run(debug=True)
