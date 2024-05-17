from flask import Flask, render_template, jsonify, request
import json

app = Flask(__name__)

# Load mental health data
with open('static/data/mental_health_data.json') as f:
    mental_health_data = json.load(f)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/data', methods=['GET'])
def get_data():
    return jsonify(mental_health_data)

if __name__ == '__main__':
    app.run(debug=True)
