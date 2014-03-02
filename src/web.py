import pandas as pd
import json
from flask import Flask, render_template, jsonify
app = Flask(__name__)

import config

# Parsing raw CSV file
db = pd.read_csv(config.db_path)

@app.route("/")
def index():
    return render_template('index.html')

@app.route("/api/points")
def get_data():
    rows = json.loads(db[:100].to_json(orient='index'))
    return jsonify(ok=True, points=rows)

if __name__ == "__main__":
    app.run(debug=True)
