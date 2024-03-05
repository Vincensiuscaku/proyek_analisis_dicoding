import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

# Loading required dataset
dataset_hour = pd.read_csv("Proyek_analisis_data_bike_sharing.csv")

# Convert 'dteday' to datetime format
dataset_hour['dteday'] = pd.to_datetime(dataset_hour['dteday'])

# Title
st.title("BICYCLE RENTAL ANALYSIS")

# Sidebar for Filters
st.sidebar.title("Filters")

# Select Year
selected_yr = st.sidebar.radio("Select Year", [2011, 2012])

# Select Date
unique_dates = sorted(dataset_hour[dataset_hour['yr'] == (selected_yr - 2011)]['dteday'].dt.date.unique())
selected_date = st.sidebar.selectbox("Select Date", unique_dates)

# Select other filters
selected_weathersit = st.sidebar.selectbox("Select Weathersit Condition", dataset_hour['weathersit'].unique())
selected_season = st.sidebar.selectbox("Select Season", dataset_hour['season'].unique())
selected_hr = st.sidebar.slider("Select Hour", 0, 23, (0, 23))
selected_temp = st.sidebar.slider("Select Temperature", 0.0, 1.0, (0.0, 1.0))

# Filter dataset based on selected filters
filtered_data = dataset_hour[
    (dataset_hour['yr'] == (selected_yr - 2011)) &  # Convert to 0-based index
    (dataset_hour['dteday'].dt.date == selected_date) &
    (dataset_hour['weathersit'] == selected_weathersit) &
    (dataset_hour['season'] == selected_season) &
    (dataset_hour['hr'].between(selected_hr[0], selected_hr[1])) &
    (dataset_hour['temp'].between(selected_temp[0], selected_temp[1]))
]

# Calculate Metrics
total_casual = int(filtered_data['casual'].sum())
total_registered = int(filtered_data['registered'].sum())
total_cnt = int(filtered_data['cnt'].sum())

# Display Metrics
st.write("##### Metrics")
col1, col2, col3 = st.columns(3)
with col1:
    st.metric("Total Casual Rentals", total_casual, "casual")
with col2:
    st.metric("Total Registered Rentals", total_registered, "registered")
with col3:
    st.metric("Total Rentals", total_cnt, "total")

# Plotting with Plotly
fig = px.line(filtered_data, x='hr', y=['casual', 'registered', 'cnt'], labels={'value': 'Count', 'variable': 'Rental Type'}, title='Casual, Registered, and Total Rentals by Hour')
st.plotly_chart(fig)

# Display filtered data
st.write("##### Filtered Data")
st.write(filtered_data)
