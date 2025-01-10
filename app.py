from flask import Flask, jsonify, render_template
import pandas as pd

app = Flask(__name__)

# Load and preprocess data
df = pd.read_csv("Student Mental health.csv")
newnames = ["Timestamp", "Gender", "Age", "Major", "Year", "CGPA", "Married", "Depression", "Anxiety", "Panic Attacks", "Treated"]
df.columns = newnames

def to_binary(d):
    return 1 if d == "Yes" else 0

for col in ["Married", "Depression", "Anxiety", "Panic Attacks", "Treated"]:
    df[col] = df[col].apply(to_binary)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/data', methods=['GET'])
def get_data():
    venn_data = {
        "Depressed": list(df[df["Depression"] == 1].index),
        "Anxious": list(df[df["Anxiety"] == 1].index),
        "PanicAttacks": list(df[df["Panic Attacks"] == 1].index)
    }

    bar_data = {
        "labels": ['Depressed', 'Anxious', 'Panic Attack'],
        "male": [
            len(df[(df["Depression"] == 1) & (df["Gender"] == "Male")]),
            len(df[(df["Anxiety"] == 1) & (df["Gender"] == "Male")]),
            len(df[(df["Panic Attacks"] == 1) & (df["Gender"] == "Male")])
        ],
        "female": [
            len(df[(df["Depression"] == 1) & (df["Gender"] == "Female")]),
            len(df[(df["Anxiety"] == 1) & (df["Gender"] == "Female")]),
            len(df[(df["Panic Attacks"] == 1) & (df["Gender"] == "Female")])
        ]
    }

    pie_data = {
        "labels": ['Female - Treated', 'Female - Not Treated', 'Male - Treated', 'Male - Not Treated'],
        "values": [
            len(df[(df["Gender"] == "Female") & (df["Treated"] == 1)]),
            len(df[(df["Gender"] == "Female") & (df["Treated"] == 0)]),
            len(df[(df["Gender"] == "Male") & (df["Treated"] == 1)]),
            len(df[(df["Gender"] == "Male") & (df["Treated"] == 0)])
        ]
    }

    return jsonify({"venn": venn_data, "bar": bar_data, "pie": pie_data})

if __name__ == '__main__':
    app.run(debug=True)
