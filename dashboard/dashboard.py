import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
from sklearn.preprocessing import LabelEncoder

sns.set_style('darkgrid')

# Load Data
students = pd.read_csv('https://github.com/nurkholiqaganihafid/Analysis_Student_Dropout_Rates/blob/main/dashboard/students.csv')

def display_dataframe(option):
    selected_student = students[students['status'].isin(option)]

    if option:
        col1, col2, col3 = st.columns(3)

        # Number of students
        with col1:
            total_students = selected_student.shape[0]
            st.metric('#Total Students', value=total_students)

        # Number of genders
        with col2:
            female_count = selected_student[selected_student['gender'] == 0].shape[0]
            st.metric('#Total Female', value=female_count)

        with col3:
            male_count = selected_student[selected_student['gender'] == 1].shape[0]
            st.metric('#Total Male', value=male_count)

        st.dataframe(selected_student)

def plot_status_bar_chart(option=None):
    if not option:
        students_status = students['status'].value_counts()
    else:
        selected_student = students[students['status'].isin(option)]
        students_status = selected_student['status'].value_counts()

    status_colors = {
        'Graduate': '#eeb9b9',
        'Dropout': '#c71416',
        'Enrolled': '#eeb9b9'
    }

    fig, ax = plt.subplots(figsize=(16,16))

    sns.barplot(
        x=students_status.index,
        y=students_status,
        palette=status_colors,
        ax=ax
    )

    ax.set_title('Number of Students by Status', fontsize=40, pad=16)
    ax.set_xlabel(None)
    ax.set_ylabel(None)
    ax.tick_params(axis='y', labelsize=30)
    ax.tick_params(axis='x', labelsize=28, pad=16)

    for i, status in enumerate(students_status.index):
        count = students_status[status]
        plt.text(i, count+5, str(count), ha='center', va='bottom', fontsize=24)

    st.pyplot(fig)

def plot_gender_bar_chart(option=None):
    if not option:
        gender_counts = students['gender'].value_counts()
        gender_counts.index = ['Female', 'Male']
    else:
        selected_student = students[students['status'].isin(option)]
        gender_counts = selected_student['gender'].value_counts()
        gender_counts.index = ['Female', 'Male']

    fig, ax = plt.subplots(figsize=(12,12))

    sns.barplot(
        x=gender_counts.index,
        y=gender_counts,
        palette=['#e38a8b'],
        ax=ax
    )

    ax.set_title('Number of Students by Gender', fontsize=30, pad=16)
    ax.set_xlabel(None)
    ax.set_ylabel(None)
    ax.tick_params(axis='y', labelsize=26)
    ax.tick_params(axis='x', labelsize=24, pad=14)

    for i, status in enumerate(gender_counts.index):
        count = gender_counts[status]
        plt.text(i, count+5, str(count), ha='center', va='bottom', fontsize=22)

    st.pyplot(fig)

def plot_status_pie_chart(option=None):
    if not option:
        students_status = students['status'].value_counts()
    else:
        selected_student = students[students['status'].isin(option)]
        students_status = selected_student['status'].value_counts()

    status_colors = {
        'Graduate': '#eeb9b9',
        'Enrolled': '#eeb9b9',
        'Dropout': '#c71416',
    }

    fig, ax = plt.subplots(figsize=(24, 18))
    sorted_labels = ['Graduate', 'Enrolled', 'Dropout']
    sorted_data = students_status.loc[students_status.index.isin(sorted_labels)]

    # Plot diagram pie jika label ada dalam indeks
    wedges, label_texts, value_texts = ax.pie(
        sorted_data,
        colors=[status_colors[label] for label in sorted_data.index if label in status_colors],
        labels=sorted_data.index,
        autopct=lambda p: f'{p:.2f}%',
        startangle=90,
    )
    ax.set_title('Comparison of Student Percentages by Status', fontsize=46, pad=16)
    ax.axis('equal')

    for text in label_texts:
        text.set_fontsize(40)

    for value_text in value_texts:
        value_text.set_fontsize(38)

    st.pyplot(fig)

def plot_gender_pie_chart(option=None):
    if not option:
        gender_counts = students['gender'].value_counts()
        gender_counts.index = ['Female', 'Male']
    else:
        selected_student = students[students['status'].isin(option)]
        gender_counts = selected_student['gender'].value_counts()
        gender_counts.index = ['Female', 'Male']

    fig, ax = plt.subplots(figsize=(24, 18))
    wedges, label_texts, value_texts = ax.pie(
        gender_counts,
        colors=['#e38a8b'],
        labels=gender_counts.index,
        autopct=lambda p: f'{p:.2f}%',
        startangle=90,
        explode=(0, 0.05)
    )
    ax.set_title('Comparison of Student Percentages by Gender', fontsize=48, pad=16)
    ax.axis('equal')

    for text in label_texts:
        text.set_fontsize(42)

    for value_text in value_texts:
        value_text.set_fontsize(40)

    st.pyplot(fig)

def plot_correlation_heatmap():
    label_encoder = LabelEncoder()
    students['status_encoded'] = label_encoder.fit_transform(students['status'])
    students.drop(columns=['status'], inplace=True)
    students.rename(columns={'status_encoded': 'status'}, inplace=True)

    correlation_matrix = students.corr()

    min_value = min(correlation_matrix['status'])
    max_value = max(correlation_matrix['status'])

    selected_range = st.slider(
        'Select correlation range by status',
        min_value, max_value,
        (min_value, max_value)
    )

    fig, ax = plt.subplots(figsize=(16, 12))
    sns.heatmap(
        correlation_matrix,
        vmin=-1.,
        vmax=1.,
        annot=False,
        cmap='coolwarm',
        linewidths=0.5,
        mask=(correlation_matrix['status'] < selected_range[0]) | (correlation_matrix['status'] > selected_range[1])
    )
    ax.set_title('Students Data Correlation', fontsize=28, pad=16)
    ax.tick_params(axis='y', labelsize=18)
    ax.tick_params(axis='x', labelsize=18)

    st.pyplot(fig)

# Streamlit App
st.header(':books: Dropout Student Analysis Dashboard :books:')
st.subheader('Detail Data')

expander = st.expander("DataFrame")
with expander:
    option = st.multiselect('Select Student Status', students['status'].unique())
    display_dataframe(option)

st.subheader('Number of Students by Status and Gender')

col1, col2 = st.columns(2)

with col1:
    plot_status_bar_chart(option)

with col2:
    plot_gender_bar_chart(option)

st.subheader('Comparison of Student Percentages by Status and Gender')

col1, col2 = st.columns(2)

with col1:
    plot_status_pie_chart(option)

with col2:
    plot_gender_pie_chart(option)

st.subheader('Students Data Correlation')
plot_correlation_heatmap()

st.caption('Copyright 2023 | Author: Nurkholiq Agani Hafid')