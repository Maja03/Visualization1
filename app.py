from flask import Flask, send_file, jsonify
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib_venn import venn3
import plotly.express as px
import io
import base64

app = Flask(__name__)

df = pd.read_csv("Student Mental health.csv")

newnames = ["Timestamp", "Gender", "Age", "Major", "Year", "CGPA", "Married", "Depression", "Anxiety", "Panic Attacks", "Treated"]
df.columns = newnames

def to_binary(d):
    if d == "Yes": return 1
    if d == "No": return 0

df["Married"] = df["Married"].apply(to_binary)
df["Depression"] = df["Depression"].apply(to_binary)
df["Anxiety"] = df["Anxiety"].apply(to_binary)
df["Panic Attacks"] = df["Panic Attacks"].apply(to_binary)
df["Treated"] = df["Treated"].apply(to_binary)

def updateVennDiagram():
    depressed = df[df["Depression"] == 1]
    anxious = df[df["Anxiety"] == 1]
    panicking = df[df["Panic Attacks"] == 1]

    plt.figure()
    venn3(subsets = [set(depressed.index), 
                    set(anxious.index), 
                    set(panicking.index)], 
        set_labels = ("Depressed", "Anxious", "Having Panic Attacks"),
        set_colors = ("orange", "purple", "green"),
        alpha = 0.9)

    plt.title("Conditions", fontsize = 16)
    buffer = io.BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    plt.close()
    return base64.b64encode(buffer.getvalue()).decode()

def updateBarChart():
    labels = ['Depressed', 'Anxious', 'Panic Attack', 'Depressed and Anxious', 'Depressed and Panic Attack', 'Anxious and Panic Attack', 'All Three', 'None']
    x = np.arange(len(labels))
    width = 0.35

    depressed = df[df["Depression"] == 1]
    anxious = df[df["Anxiety"] == 1]
    panicking = df[df["Panic Attacks"] == 1]

    has_condition = pd.concat([depressed, anxious, panicking]).drop_duplicates()

    only_depressed = depressed[(depressed["Anxiety"] == 0) & (depressed["Panic Attacks"] == 0)]
    only_anxious = anxious[(anxious["Depression"] == 0) & (anxious["Panic Attacks"] == 0)]
    only_panicking = panicking[(panicking["Depression"] == 0) & (panicking["Anxiety"] == 0)]
    depressed_anxious = depressed[(depressed["Anxiety"] == 1) & (depressed["Panic Attacks"] == 0)]
    depressed_panicking = depressed[(depressed["Anxiety"] == 0) & (depressed["Panic Attacks"] == 1)]
    anxious_panicking = anxious[(anxious["Depression"] == 0) & (anxious["Panic Attacks"] == 1)]
    all_three = has_condition[(has_condition["Depression"] == 1) & (has_condition["Anxiety"] == 1) & (has_condition["Panic Attacks"] == 1)]
    none = has_condition[(has_condition["Depression"] == 0) & (has_condition["Anxiety"] == 0) & (has_condition["Panic Attacks"] == 0)]

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

    plt.figure(figsize=(10, 6))
    rects1 = plt.bar(x - width/2, male_counts, width, label='Male', color='gray')
    rects2 = plt.bar(x + width/2, female_counts, width, label='Female', color='orange')

    def autolabel(rects):
        for rect in rects:
            height = rect.get_height()
            plt.annotate('{}'.format(height),
                        xy=(rect.get_x() + rect.get_width() / 2, height),
                        xytext=(0, 3),  # 3 points vertical offset
                        textcoords="offset points",
                        ha='center', va='bottom')

    autolabel(rects1)
    autolabel(rects2)

    plt.ylabel('Number of people')
    plt.title('Number of people with different combinations of mental states for men and women')
    plt.xticks(x, labels, rotation=45, ha='right')
    plt.legend()
    
    buffer = io.BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    plt.close()
    return base64.b64encode(buffer.getvalue()).decode()

def updatePieChart():
    female_data = df[df["Gender"] == "Female"]
    male_data = df[df["Gender"] == "Male"]

    female_treated = female_data[female_data["Treated"] == 1].shape[0]
    female_not_treated = female_data[female_data["Treated"] == 0].shape[0]
    male_treated = male_data[male_data["Treated"] == 1].shape[0]
    male_not_treated = male_data[male_data["Treated"] == 0].shape[0]

    labels = ['Female - Treated', 'Female - Not Treated', 'Male - Treated', 'Male - Not Treated']
    Count = [female_treated, female_not_treated, male_treated, male_not_treated]

    fig = px.pie(names=labels, values=Count, title='Number of people undergoing and not undergoing treatment, by gender')
    fig.update_traces(textposition='inside', 
                    textinfo='percent+value',  
                    marker=dict(line=dict(color='#FFFFFF', width=2)),  
                    textfont_size=12) 
    
    buffer = io.BytesIO()
    fig.write_image(buffer, format='png')
    buffer.seek(0)
    plt.close()
    return base64.b64encode(buffer.getvalue()).decode()

@app.route('/')
def index():
    return send_file('index.html')

@app.route('/data', methods=['GET'])
def get_data():
    venn_diagram = updateVennDiagram()
    bar_chart = updateBarChart()
    pie_chart = updatePieChart()
    return jsonify(venn_diagram=venn_diagram, bar_chart=bar_chart, pie_chart=pie_chart)

if __name__ == '__main__':
    app.run(debug=True)

