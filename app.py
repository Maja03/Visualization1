from flask import Flask, send_file, jsonify
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib_venn import venn3
import plotly.express as px

app = Flask(__name__)

# Wczytaj dane mentalne z pliku CSV
df = pd.read_csv("Student Mental health.csv")

# Przetwórz dane
newnames = ["Timestamp", "Gender", "Age", "Major", "Year", "CGPA", "Married", "Depression", "Anxiety", "Panic Attacks", "Treated"]
df.columns = newnames

# Przetwórz kolumny na format binarny
def to_binary(d):
    if d == "Yes": return 1
    if d == "No": return 0

df["Married"] = df["Married"].apply(to_binary)
df["Depression"] = df["Depression"].apply(to_binary)
df["Anxiety"] = df["Anxiety"].apply(to_binary)
df["Panic Attacks"] = df["Panic Attacks"].apply(to_binary)
df["Treated"] = df["Treated"].apply(to_binary)

@app.route('/')
def index():
    return send_file('index.html')

@app.route('/data', methods=['GET'])
def get_data():
    updateVennDiagram()
    updateBarChart()
    updatePieChart()
    return jsonify(success=True)

if __name__ == '__main__':
    app.run(debug=True)

# Funkcja do aktualizacji wizualizacji Vennowskiego diagramu
def updateVennDiagram():
    depressed = df[df["Depression"] == 1]
    anxious = df[df["Anxiety"] == 1]
    panicking = df[df["Panic Attacks"] == 1]

    only_depressed = depressed[(depressed["Anxiety"] == 0) & (depressed["Panic Attacks"] == 0)]
    only_anxious = anxious[(anxious["Depression"] == 0) & (anxious["Panic Attacks"] == 0)]
    only_panicking = panicking[(panicking["Depression"] == 0) & (panicking["Anxiety"] == 0)]
    depressed_anxious = depressed[(depressed["Anxiety"] == 1) & (depressed["Panic Attacks"] == 0)]
    depressed_panicking = depressed[(depressed["Anxiety"] == 0) & (depressed["Panic Attacks"] == 1)]
    anxious_panicking = anxious[(anxious["Depression"] == 0) & (anxious["Panic Attacks"] == 1)]
    all_three = df[(df["Depression"] == 1) & (df["Anxiety"] == 1) & (df["Panic Attacks"] == 1)]
    none = df[(df["Depression"] == 0) & (df["Anxiety"] == 0) & (df["Panic Attacks"] == 0)]

    venn3(subsets=[set(only_depressed.index),
                   set(only_anxious.index),
                   set(only_panicking.index)],
          set_labels=("Depressed", "Anxious", "Having Panic Attacks"),
          set_colors=("orange", "purple", "green"),
          alpha=0.9)

    plt.title("Conditions", fontsize=16)
    plt.savefig('venn_diagram.png')

# Funkcja do aktualizacji wykresu słupkowego
def updateBarChart():
    labels = ['Depressed', 'Anxious', 'Panic Attack', 'Depressed and Anxious', 'Depressed and Panic Attack', 'Anxious and Panic Attack', 'All Three', 'None']
    x = np.arange(len(labels))
    width = 0.35

    male_counts = [
        len(only_depressed[only_depressed["Gender"] == "Male"]),
        len(only_anxious[only_anxious["Gender"] == "Male"]),
        len(only_panicking[only_panicking["Gender"] == "Male"]),
        len(depressed_anxious[depressed_anxious["Gender"] == "Male"]),
        len(depressed_panicking[depressed_panicking["Gender"] == "Male"]),
        len(anxious_panicking[anxious_panicking["Gender"] == "Male"]),
        len(all_three[all_three["Gender"] == "Male"]),
        len(none[none["Gender"] == "Male"])
    ]
    female_counts = [
        len(only_depressed[only_depressed["Gender"] == "Female"]),
        len(only_anxious[only_anxious["Gender"] == "Female"]),
        len(only_panicking[only_panicking["Gender"] == "Female"]),
        len(depressed_anxious[depressed_anxious["Gender"] == "Female"]),
        len(depressed_panicking[depressed_panicking["Gender"] == "Female"]),
        len(anxious_panicking[anxious_panicking["Gender"] == "Female"]),
        len(all_three[all_three["Gender"] == "Female"]),
        len(none[none["Gender"] == "Female"])
    ]

    fig, ax = plt.subplots(figsize=(10, 6))
    rects1 = ax.bar(x - width/2, male_counts, width, label='Male', color='gray')
    rects2 = ax.bar(x + width/2, female_counts, width, label='Female', color='orange')

    def autolabel(rects):
        for rect in rects:
            height = rect.get_height()
            ax.annotate('{}'.format(height),
                        xy=(rect.get_x() + rect.get_width() / 2, height),
                        xytext=(0, 3),  # 3 points vertical offset
                        textcoords="offset points",
                        ha='center', va='bottom')

    autolabel(rects1)
    autolabel(rects2)

    ax.set_ylabel('Number of people')
    ax.set_title('Number of people with different combinations of mental states for men and women')
    ax.set_xticks(x)
    ax.set_xticklabels(labels, rotation=45, ha='right')
    ax.legend()
    plt.savefig('bar_chart.png')

# Funkcja do aktualizacji wykresu kołowego
def updatePieChart():
    female_treated = df[(df["Gender"] == "Female") & (df["Treated"] == 1)].shape[0]
    female_not_treated = df[(df["Gender"] == "Female") & (df["Treated"] == 0)].shape[0]
    male_treated = df[(df["Gender"] == "Male") & (df["Treated"] == 1)].shape[0]
    male_not_treated = df[(df["Gender"] == "Male") & (df["Treated"] == 0)].shape[0]

    df_plot = pd.DataFrame({
        'Gender': ['Female - Treated', 'Female - Not Treated', 'Male - Treated', 'Male - Not Treated'],
        'Count': [female_treated, female_not_treated, male_treated, male_not_treated]
    })
    fig = px.pie(df_plot, values='Count', names='Gender', title='Number of people undergoing and not undergoing treatment, by gender')
    fig.show()
@app.route('/')
def index():
    return send_file('index.html')

@app.route('/data', methods=['GET'])
def get_data():
    updateVennDiagram()
    updateBarChart()
    updatePieChart()
    return jsonify(success=True)

if __name__ == '__main__':
    app.run(debug=True)

