from flask import Flask, render_template
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib_venn import venn3
import plotly.express as px
import plotly.io as pio

app = Flask(__name__)

# Example DataFrame (replace with your actual data loading logic)
data = {
    "Gender": ["Male", "Female", "Male", "Female", "Male"],
    "Depressed": [1, 1, 0, 0, 1],
    "Anxious": [1, 0, 1, 0, 1],
    "Panicking": [0, 1, 1, 0, 0],
}
df = pd.DataFrame(data)

# Subsets
depressed = df[df["Depressed"] == 1]
anxious = df[df["Anxious"] == 1]
panicking = df[df["Panicking"] == 1]
depressed_anxious = depressed[depressed["Anxious"] == 1]
depressed_panicking = depressed[depressed["Panicking"] == 1]
anxious_panicking = anxious[anxious["Panicking"] == 1]
all_three = depressed[depressed["Anxious"] & depressed["Panicking"]]

# Function to generate Venn Diagram
def create_venn_diagram():
    plt.figure(figsize=(8, 6))
    venn = venn3(
        subsets=(
            len(depressed),
            len(anxious),
            len(depressed_anxious),
            len(panicking),
            len(depressed_panicking),
            len(anxious_panicking),
            len(all_three),
        ),
        set_labels=("Depressed", "Anxious", "Panicking"),
    )
    plt.title("Venn Diagram of Mental Health Conditions")
    plt.savefig("static/venn_plot.png")
    plt.close()

# Function to generate interactive charts with Plotly
def create_interactive_charts():
    categories = [
        "Depressed",
        "Anxious",
        "Panicking",
        "Depressed and Anxious",
        "Depressed and Panicking",
        "Anxious and Panicking",
        "All Three",
    ]
    subsets = [
        depressed,
        anxious,
        panicking,
        depressed_anxious,
        depressed_panicking,
        anxious_panicking,
        all_three,
    ]

    male_counts = [len(subset[subset["Gender"] == "Male"]) for subset in subsets]
    female_counts = [len(subset[subset["Gender"] == "Female"]) for subset in subsets]

    # Males
    fig_males = px.pie(
        names=categories,
        values=male_counts,
        title="Conditions Among Males",
        color_discrete_sequence=px.colors.qualitative.Set3,
    )
    pio.write_html(fig_males, file="templates/pie_chart_males.html", auto_open=False)

    # Females
    fig_females = px.pie(
        names=categories,
        values=female_counts,
        title="Conditions Among Females",
        color_discrete_sequence=px.colors.qualitative.Set3,
    )
    pio.write_html(fig_females, file="templates/pie_chart_females.html", auto_open=False)

@app.route("/")
def index():
    create_venn_diagram()
    return render_template("index.html")

@app.route("/males")
def males():
    create_interactive_charts()
    return render_template("pie_chart_males.html")

@app.route("/females")
def females():
    create_interactive_charts()
    return render_template("pie_chart_females.html")

if __name__ == "__main__":
    app.run(debug=True)
