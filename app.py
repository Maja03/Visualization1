from flask import Flask, render_template
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib_venn import venn3

app = Flask(__name__)

# Load the data
df = pd.read_csv('Student Mental health.csv')

# Rename columns
newnames = ["Timestamp", "Gender", "Age", "Major", "Year", "CGPA", "Married", "Depression", "Anxiety", "Panic Attacks", "Treated"]
df.columns = newnames

# Convert "Yes"/"No" to 1/0
def to_binary(d):
    return 1 if d == "Yes" else 0

df["Married"] = df["Married"].apply(to_binary)
df["Depression"] = df["Depression"].apply(to_binary)
df["Anxiety"] = df["Anxiety"].apply(to_binary)
df["Panic Attacks"] = df["Panic Attacks"].apply(to_binary)
df["Treated"] = df["Treated"].apply(to_binary)
df["Year"] = df["Year"].str[-1:]

# Create subsets for conditions
depressed = df[df["Depression"] == 1]
anxious = df[df["Anxiety"] == 1]
panicking = df[df["Panic Attacks"] == 1]

# Combined conditions
depressed_anxious = df[(df["Depression"] == 1) & (df["Anxiety"] == 1)]
depressed_panicking = df[(df["Depression"] == 1) & (df["Panic Attacks"] == 1)]
anxious_panicking = df[(df["Anxiety"] == 1) & (df["Panic Attacks"] == 1)]
all_three = df[(df["Depression"] == 1) & (df["Anxiety"] == 1) & (df["Panic Attacks"] == 1)]

# Venn diagram plot
def create_venn():
    plt.figure(figsize=(8, 6))
    venn3(
        subsets=[set(depressed.index), set(anxious.index), set(panicking.index)],
        set_labels=("Depressed", "Anxious", "Having Panic Attacks"),
        set_colors=("orange", "purple", "green"),
        alpha=0.9
    )
    plt.title("Conditions", fontsize=16)
    plt.savefig("static/venn_plot.png")
    plt.close()

# Generate pie charts
def create_pie_charts():
    categories = ['Depressed', 'Anxious', 'Panicking', 'Depressed and Anxious', 'Depressed and Panicking', 'Anxious and Panicking', 'All Three']
    subsets = [depressed, anxious, panicking, depressed_anxious, depressed_panicking, anxious_panicking, all_three]

    male_counts = [len(subset[subset["Gender"] == "Male"]) for subset in subsets]
    female_counts = [len(subset[subset["Gender"] == "Female"]) for subset in subsets]

    fig, axs = plt.subplots(2, 1, figsize=(12, 8))
    axs[0].pie(male_counts, labels=categories, autopct='%1.1f%%', startangle=90)
    axs[0].set_title('Conditions Among Males')
    axs[1].pie(female_counts, labels=categories, autopct='%1.1f%%', startangle=90)
    axs[1].set_title('Conditions Among Females')

    plt.tight_layout()
    plt.savefig("static/pie_chart.png")
    plt.close()

@app.route('/')
def index():
    create_venn()
    create_pie_charts()
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
