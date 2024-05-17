from flask import Flask, send_file, jsonify
import pandas as pd

app = Flask(__name__)

# Load mental health data from CSV
mental_health_data = pd.read_csv('Student Mental health.csv')
mental_health_json = mental_health_data.to_json(orient='records')

@app.route('/')
def index():
    return send_file('index.html')

@app.route('/data', methods=['GET'])
def get_data():
    return jsonify(mental_health_json)

if __name__ == '__main__':
    app.run(debug=True)
