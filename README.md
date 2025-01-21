# Student Mental Health Survey Data

This project visualizes data from a survey of university students, focusing on mental health issues, demographic factors, and academic performance. The application helps identify patterns and trends to better understand the challenges faced by students.

## Dataset Overviev

The dataset contains responses about students’ demographics, academic details, and mental health, including:

- **Demographic**s: Gender, age, marital status.
- **Academics**: Course, year of study, CGPA (Cumulative Grade Point Average).
- **Mental Health**: Self-reported conditions (depression, anxiety, panic attacks) and whether the student sought treatment.
- **Timestamp**: Captures when the response was submitted.

## Key User Groups

The application focuses on the following user groups:

- **Gender**: The dataset includes both male and female students.
- **Age**: Ages range from 18 to 24, covering typical university-age students.
- **Courses**: Students are enrolled in a variety of courses such as Engineering, Islamic Education, BIT (Business Information Technology), Laws, Mathematics, Human Resources, Psychology, Biomedical Science, and more.
- **Years of Study**: The respondents are in different stages of their university education, from year 1 to year 4.

## User Objectives

Understanding the user objectives involves examining the motivations behind the survey responses. These include:

- **Assessing Mental Health**: Students are sharing their mental health status, including whether they suffer from depression, anxiety, or panic attacks.
- **Seeking Support**: The dataset indicates whether students have sought specialist treatment for their mental health issues, reflecting their proactive steps towards managing their well-being.
- **Academic Performance**: By providing their CGPA, students' academic performance is highlighted, which could be correlated with their mental health status.
- **Demographic Insights**: The data gives an overview of the demographic distribution of students, which can be used to identify patterns and trends among different groups.

## Features of Visualization Tool

1. **Venn Diagram of Mental Health Conditions**
Shows overlaps between students with depression, anxiety, and panic attacks.
Highlights intersectional challenges (e.g., students experiencing all three conditions).

2. **Gender-Specific Pie Charts**
Visualizes the proportion of males and females with various mental health conditions.
Explores patterns in treatment-seeking behavior.

3. **Interactive and User-Friendly UI**
Users can switch between Venn diagrams and gender-specific pie charts.
Charts dynamically update based on the backend data.

## Technical Implementation

- **Backend**: A two-tier architecture using Flask for serving data.
- **Frontend**: D3.js for interactive and customizable visualizations.
- **Data Transformation**: Binary encoding for mental health conditions and data cleaning for consistent analysis.