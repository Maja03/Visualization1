import pandas as pd
from flask import Flask, render_template, jsonify


mental_health_data = pd.read_csv('Student Mental health.csv')
mental_health_json = mental_health_data.to_json(orient='records')

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/data', methods=['GET'])
def get_data():
    return jsonify(mental_health_json)

if __name__ == '__main__':
    app.run(debug=True)
