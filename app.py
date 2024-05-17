from flask import Flask, send_file, jsonify, request
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
    chart_type = request.args.get('chart')  # Odczytaj parametr chart z zapytania

    # Sprawdź, jaki typ wykresu został żądany
    if chart_type == 'bar':
        bar_chart_data = [
            {"label": "Category 1", "value": 10},
            {"label": "Category 2", "value": 20},
            {"label": "Category 3", "value": 15}
        ]
        return jsonify(bar_chart_data)
    else:
        return jsonify(mental_health_json)

if __name__ == '__main__':
    app.run(debug=True)
