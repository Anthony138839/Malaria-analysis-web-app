# Importing dependencies
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import streamlit as st

def malaria_dist():
    st.header("Exploratory Data Analysis for a Malaria dataset")
    malaria_dataset = pd.read_csv("estimated_numbers.csv")
    
    # Handling missing values
    malaria_dataset = malaria_dataset.dropna()
    st.dataframe(malaria_dataset)

    
    # Function to create button to generate the rows and columns of the dataset
    def createButton():
        if st.button("Dimension of dataset"):
            st.write(f"Number of rows and columns of the dataset: {malaria_dataset.shape}")
    createButton()
    
    # Function to generate a heatmap
    def correlation(malaria_dataset):
        # nonlocal malaria_dataset
        st.subheader("Correlation of cases and deaths")

        # Define the correlation matrix
        correlation_col = malaria_dataset[["No. of cases_median", "No. of cases_min", "No. of cases_max", "No. of deaths_median", "No. of deaths_min", "No. of deaths_max"]]
        correlation_matrix = correlation_col.corr()
        
        # Constructing the heatmap
        fig = plt.figure(figsize=(10, 6))
        sns.heatmap(correlation_matrix, cbar=True, annot=True, square=True, fmt=".2f", cmap="Blues")
        st.pyplot(fig)
    correlation(malaria_dataset)
    
    # Function to drop columns
    def dropColumns(malaria_dataset):
        st.subheader("Updated Dataset")
        
        # Dropping the unnecesssary columns
        malaria_dataset = malaria_dataset.drop(columns=["No. of cases", "No. of cases_min", "No. of cases_max", "No. of deaths", "No. of deaths_min", "No. of deaths_max"], axis=1)
        
        # Renaming some columns
        malaria_dataset = malaria_dataset.rename(columns={"No. of cases_median": "No. of cases", "No. of deaths_median": "No. of deaths"})
        st.dataframe(malaria_dataset)
        return malaria_dataset
    
    # The newly updated dataset
    malaria_dataset = dropColumns(malaria_dataset)

    # Function to generate a bar chart
    def barchart(malaria_dataset):
        # Setting up the x- and y- axes
        numeric_col_1 = ["No. of cases", "No. of deaths"]
        x1_axis = st.selectbox("Select a column for the horizontal bar chart:", numeric_col_1)
        y1_axis = "WHO Region"
        
        # Creating a header
        st.subheader(f"Distribution of {x1_axis} based on WHO Region")
        
        # Bar chart
        fig1 = px.bar(malaria_dataset, x=x1_axis, y=y1_axis, color=y1_axis)
        st.plotly_chart(fig1)
    barchart(malaria_dataset)
    
    # Function to generate a pie chart
    def piechart(malaria_dataset):
        # Setting up the x- and y- axes
        numeric_col_2 = ["No. of cases", "No. of deaths"]
        x2_axis = "WHO Region"
        y2_axis = st.selectbox("Select a column for the pie chart:", numeric_col_2)
        new_group = malaria_dataset.groupby("WHO Region")[y2_axis].sum().reset_index()
        
        # Creating a header
        st.subheader(f"Distribution of {y2_axis} based on WHO Region")
        
        # Pie chart
        fig2 = px.pie(new_group, values=y2_axis, names=x2_axis)
        st.plotly_chart(fig2)
    piechart(malaria_dataset)
    
    # Function to generate the top 10 countries with less malaria cases and deaths
    def lessCases(malaria_dataset):
        numeric_col_3 = ["No. of cases", "No. of deaths"]
        bar_cases_and_deaths = malaria_dataset.groupby("Country")[numeric_col_3].sum().reset_index()
        less_10 = bar_cases_and_deaths.nsmallest(10, "No. of cases")
        x3_axis = "Country"
        y3_axis = st.selectbox("Select a column for the bar chart", numeric_col_3)
        
          # Creating a header
        st.subheader(f"Distribution of top 10 countries with less {y3_axis}")
        
        # Bar chart
        fig3 = px.bar(less_10, x=x3_axis, y=y3_axis, color=y3_axis)
        st.plotly_chart(fig3)
    lessCases(malaria_dataset)
    
    def mostCases(malaria_dataset):
        numeric_col_4 = ["No. of cases", "No. of deaths"]
        new_bar_cases_and_deaths = malaria_dataset.groupby("Country")[numeric_col_4].sum().reset_index()
        top_10 = new_bar_cases_and_deaths.nlargest(10, "No. of cases")
        x4_axis = "Country"
        y4_axis = st.selectbox("Select a column for the new bar chart", numeric_col_4)
        
          # Creating a header
        st.subheader(f"Distribution of top 10 countries with most {y4_axis}")
        
        # Bar chart
        fig4 = px.bar(top_10, x=x4_axis, y=y4_axis, color=x4_axis)
        st.plotly_chart(fig4)
    mostCases(malaria_dataset)
    
    # Function to generate trend analysis
    def trend(malaria_dataset):
        # Create a range slider 
        min_year = malaria_dataset["Year"].min()
        max_year = malaria_dataset["Year"].max()
        
        # Create a year range
        year_range = st.slider("Select year range", min_year, max_year, (min_year, max_year))
        
        # Filter the data with respect to the year range
        filtered_data = malaria_dataset[(malaria_dataset["Year"] > year_range[0]) & (malaria_dataset["Year"] <= year_range[1])]
        
        # Setting up the x- and y- axes
        numeric_col_5 = ["No. of cases", "No. of deaths"]
        trends = filtered_data.groupby("Year")[numeric_col_5].sum().reset_index()
        
        # Constructing the trend analysis diagram
        st.subheader(f"Trend Analysis of Malaria cases and Malaria deaths from {year_range[0]} to {year_range[1]}")
        
        fig5 = plt.figure(figsize=(10,5))
        
        # Handling the first line plot
        sns.lineplot(trends, x="Year", y=numeric_col_5[0], marker="s", color="blue")
        plt.xlabel("Year")
        plt.ylabel(f"{numeric_col_5[0]}", color="blue")
        
        plt.twinx()
        
        # Handling the second line plot
        sns.lineplot(trends, x="Year", y=numeric_col_5[1], marker="o", color="green")
        plt.ylabel(f"{numeric_col_5[1]}", color="green")
        
        # Setting up the grid
        sns.set_theme(style="whitegrid")
        
        # Displaying the line plot
        st.pyplot(fig5)
    trend(malaria_dataset)
malaria_dist()