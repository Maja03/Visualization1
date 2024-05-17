import numpy as np
import pandas as pd
import matplotlib as mpl
import matplotlib.pyplot as plt
import random
import seaborn as sns
import statsmodels.stats as sm

from matplotlib_venn import venn3
from scipy import stats

df = pd.read_csv("Student Mental health.csv")
df.head()

newnames = ["Timestamp", "Gender", "Age", "Major", "Year", "CGPA", "Married", "Depression", "Anxiety", "Panic Attacks", "Treated"]
df.columns = newnames
df.head()

def to_binary(d):
    if d == "Yes"   : return 1
    if d == "No"    : return 0
    
df["Married"] = df["Married"].apply(to_binary)
df["Depression"] = df["Depression"].apply(to_binary)
df["Anxiety"] = df["Anxiety"].apply(to_binary)
df["Panic Attacks"] = df["Panic Attacks"].apply(to_binary)
df["Treated"] = df["Treated"].apply(to_binary)

df["Year"] = df["Year"].str[-1:]

df.head()

has_smtn = list()
dep_col = df.columns.get_loc("Depression")
anx_col = df.columns.get_loc("Anxiety")
pa_col = df.columns.get_loc("Panic Attacks")

for row in range(len(df.index)):
    if df.iloc[row, dep_col] == 1:
        has_smtn.append(1)
    elif df.iloc[row, anx_col] == 1:
        has_smtn.append(1)
    elif df.iloc[row, pa_col] == 1:
        has_smtn.append(1)
    else:
        has_smtn.append(0)

df["Condition"] = has_smtn
df.head()

depressed = df[(df["Depression"] == 1)]
anxious = df[(df["Anxiety"] == 1)]
panicking = df[(df["Panic Attacks"] == 1)]

has_condition = pd.concat([depressed, anxious, panicking]).drop_duplicates()
has_condition

treated_subset = has_condition.loc[df["Treated"] == 1]
print(len(treated_subset))
treated_subset

only_depressed = depressed[(depressed["Anxiety"] == 0) & (depressed["Panic Attacks"] == 0)]
only_anxious = anxious[(anxious["Depression"] == 0) & (anxious["Panic Attacks"] == 0)]
only_panicking = panicking[(panicking["Depression"] == 0) & (panicking["Anxiety"] == 0)]
depressed_anxious = depressed[(depressed["Anxiety"] == 1) & (depressed["Panic Attacks"] == 0)]
depressed_panicking = depressed[(depressed["Anxiety"] == 0) & (depressed["Panic Attacks"] == 1)]
anxious_panicking = anxious[(anxious["Depression"] == 0) & (anxious["Panic Attacks"] == 1)]
all_three = has_condition[(has_condition["Depression"] == 1) & (has_condition["Anxiety"] == 1) & (has_condition["Panic Attacks"] == 1)]
none = has_condition[(has_condition["Depression"] == 0) & (has_condition["Anxiety"] == 0) & (has_condition["Panic Attacks"] == 0)]


num_depressed = (df["Depression"] == 1).sum()
num_anxious = (df["Anxiety"] == 1).sum()
num_pa = (df["Panic Attacks"] == 1).sum()
num_treated = (df["Treated"] == 1).sum()
num_w_condition = (df["Condition"] == 1).sum()
num_wo_condition = (df["Condition"] == 0).sum()
​
print("Depressed: {}\nAnxious: {}\nHaving panic attacks: {}\nBeing treated: {}\nTotal people with a condition: {}\nTotal people without: {}".format(num_depressed, num_anxious, num_pa, num_treated, num_w_condition, num_wo_condition))

venn3(subsets = [set(depressed.index), 
                 set(anxious.index), 
                 set(panicking.index)], 
      set_labels = ("Depressed", "Anxious", "Having Panic Attacks"),
      set_colors = ("orange", "purple", "green"),
      alpha = 0.9)

plt.title("Conditions", fontsize = 16)
plt.show()

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

labels = ['Depressed', 'Anxious', 'Panic Attack', 'Depressed and Anxious', 'Depressed and Panic Attack', 'Anxious and Panic Attack', 'All Three', 'None']
x = np.arange(len(labels))
width = 0.35

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

plt.show()


import plotly.express as px
# Dane
female_data = df[df["Gender"] == "Female"]
male_data = df[df["Gender"] == "Male"]

female_treated = female_data[female_data["Treated"] == 1].shape[0]
female_not_treated = female_data[female_data["Treated"] == 0].shape[0]
male_treated = male_data[male_data["Treated"] == 1].shape[0]
male_not_treated = male_data[male_data["Treated"] == 0].shape[0]

labels = ['Female - Treated', 'Female - Not Treated', 'Male - Treated', 'Male - Not Treated']
Count = [female_treated, female_not_treated, male_treated, male_not_treated]
colors=['#FFA500', '#FFDAB9', '#808080', '#D3D3D3']

# Tworzenie wykresu kołowego
fig = px.pie(df_plot, values='Count', names='Gender', title='Number of people undergoing and not undergoing treatment, by gender')
fig.update_traces(textposition='inside', 
                  textinfo='percent+value',  # Informacje tekstowe będą zawierały procenty, etykiety i wartości
                  marker=dict(line=dict(color='#FFFFFF', width=2)),  # Dodanie białej obwódki wokół każdego kawałka
                  textfont_size=12)  # Rozmiar czcionki tekstu
            

fig.show()
