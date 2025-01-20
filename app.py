from flask import Flask, render_template, jsonify
import pandas as pd

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
panic_attacks = df[df["Panic Attacks"] == 1]

# Combined conditions
depressed_anxious = df[(df["Depression"] == 1) & (df["Anxiety"] == 1)]
depressed_panicking = df[(df["Depression"] == 1) & (df["Panic Attacks"] == 1)]
anxious_panicking = df[(df["Anxiety"] == 1) & (df["Panic Attacks"] == 1)]
all_three = df[(df["Depression"] == 1) & (df["Anxiety"] == 1) & (df["Panic Attacks"] == 1)]

# Generate Pie Charts
def create_pie_charts():
    categories = ['Depressed', 'Anxious', 'Panic Attacks', 'Depressed and Anxious', 'Depressed and Panic Attacks', 'Anxious and Panic Attacks', 'All Three']
    subsets = [
        depressed, anxious, panic_attacks,
        depressed_anxious, depressed_panicking, anxious_panicking, all_three
    ]

    male_counts = [len(subset[subset["Gender"] == "Male"]) for subset in subsets]
    female_counts = [len(subset[subset["Gender"] == "Female"]) for subset in subsets]

    # Debugging output to ensure data consistency
    print("Categories:", categories)
    print("Male Counts:", male_counts)
    print("Female Counts:", female_counts)

    return {'male_counts': male_counts, 'female_counts': female_counts, 'categories': categories}


@app.route('/')
def home():
    return render_template('index.html', chart_type="venn")

@app.route('/males')
def males():
    return render_template('index.html', chart_type="males")

@app.route('/females')
def females():
    return render_template('index.html', chart_type="females")

@app.route('/data')
def get_data():
    venn_data = {
        'depressed': len(depressed) - len(depressed_anxious) - len(depressed_panicking) + len(all_three),
        'anxious': len(anxious) - len(depressed_anxious) - len(anxious_panicking) + len(all_three),
        'panicking': len(panic_attacks) - len(depressed_panicking) - len(anxious_panicking) + len(all_three),
        'depressed_anxious': len(depressed_anxious) - len(all_three),
        'depressed_panicking': len(depressed_panicking) - len(all_three),
        'anxious_panicking': len(anxious_panicking) - len(all_three),
        'all_three': len(all_three),
    }

    pie_data = create_pie_charts()

    return jsonify({
        'venn': venn_data,
        'pie': pie_data
    })

if __name__ == '__main__':
    app.run(debug=True)
