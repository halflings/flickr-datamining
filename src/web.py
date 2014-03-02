import json
from flask import Flask, render_template, jsonify
app = Flask(__name__)

from mining import db

print db.dtypes

@app.route("/")
def index():
    return render_template('index.html')

@app.route("/api/points")
def get_data():
    rows = json.loads(db[:100].to_json(orient='index'))
    for key, row in rows.iteritems():
        row['hashtags'] = row['hashtags'].split(',') if row['hashtags'] else None
    return jsonify(ok=True, points=rows)

if __name__ == "__main__":
    app.run(debug=True)
