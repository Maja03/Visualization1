from flask import Flask, render_template
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib_venn import venn3
import random

app = Flask(__name__)

# Load the data
df = pd.read_csv('Student Mental health.csv')

# Modify column names as you have in your notebook
newnames = ["Timestamp", "Gender", "Age", "Major", "Year", "CGPA", "Married", "Depression", "Anxiety", "Panic Attacks", "Treated"]
df.columns = newnames

# Function to convert "Yes"/"No" to 1/0
def to_binary(d):
    return 1 if d == "Yes" else 0

# Apply the conversion
df["Married"] = df["Married"].apply(to_binary)
df["Depression"] = df["Depression"].apply(to_binary)
df["Anxiety"] = df["Anxiety"].apply(to_binary)
df["Panic Attacks"] = df["Panic Attacks"].apply(to_binary)
df["Treated"] = df["Treated"].apply(to_binary)
df["Year"] = df["Year"].str[-1:]

# Create the 'Condition' column
has_smtn = []
dep_col = df.columns.get_loc("Depression")
anx_col = df.columns.get_loc("Anxiety")
pa_col = df.columns.get_loc("Panic Attacks")

for row in range(len(df.index)):
    if df.iloc[row, dep_col] == 1 or df.iloc[row, anx_col] == 1 or df.iloc[row, pa_col] == 1:
        has_smtn.append(1)
    else:
        has_smtn.append(0)
df["Condition"] = has_smtn

# Create subsets for the conditions
depressed = df[(df["Depression"] == 1)]
anxious = df[(df["Anxiety"] == 1)]
panicking = df[(df["Panic Attacks"] == 1)]
has_condition = pd.concat([depressed, anxious, panicking]).drop_duplicates()

# Venn diagram plot
def create_venn():
    plt.figure(figsize=(8, 6))
    venn3(subsets=[set(depressed.index), set(anxious.index), set(panicking.index)],
          set_labels=("Depressed", "Anxious", "Having Panic Attacks"),
          set_colors=("orange", "purple", "green"), alpha=0.9)
    plt.title("Conditions", fontsize=16)
    plt.savefig("static/venn_plot.png")  # Save to static folder
    plt.close()

# Generate the pie charts
def create_pie_charts():
    categories = ['Depressed', 'Anxious', 'Panicking', 'Depressed and Anxious', 'Depressed and Panicking', 'Anxious and Panicking', 'All Three']
    male_counts = [len(df[df["Gender"] == "Male"][condition]) for condition in [depressed, anxious, panicking, depressed_anxious, depressed_panicking, anxious_panicking, all_three]]
    female_counts = [len(df[df["Gender"] == "Female"][condition]) for condition in [depressed, anxious, panicking, depressed_anxious, depressed_panicking, anxious_panicking, all_three]]

    fig, axs = plt.subplots(2, 1, figsize=(12, 8))
    axs[0].pie(male_counts, labels=categories, autopct='%1.1f%%')
    axs[0].set_title('Conditions Among Males')
    axs[1].pie(female_counts, labels=categories, autopct='%1.1f%%')
    axs[1].set_title('Conditions Among Females')

    plt.tight_layout()
    plt.savefig("static/pie_chart.png")  # Save to static folder
    plt.close()

@app.route('/')
def index():
    create_venn()  # Generate Venn plot
    create_pie_charts()  # Generate pie charts
    return render_template('index.html')  # Render the template

if __name__ == '__main__':
    app.run(debug=True)
