# app.py

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import pickle

# Load data from pickle file
@st.cache_data
def load_data():
    with open('carbon_data.pkl', 'rb') as f:
        data = pickle.load(f)
    return data

df = load_data()

# App title
st.title('Global Carbon Emissions Analysis')

# Sidebar filters
st.sidebar.header('Filters')
selected_year = st.sidebar.selectbox('Select Year', sorted(df['Year'].unique(), reverse=True))
selected_region = st.sidebar.selectbox('Select Region', ['All'] + list(df['Region'].unique()))

# Filter data based on selections
filtered_data = df[df['Year'] == selected_year]
if selected_region != 'All':
    filtered_data = filtered_data[filtered_data['Region'] == selected_region]

# Display filtered data
st.subheader('Filtered Data')
st.dataframe(filtered_data)

# Key metrics
st.subheader('Key Metrics')
col1, col2, col3 = st.columns(3)
with col1:
    st.metric("Total Emissions (Kilotons)", f"{filtered_data['Kilotons of Co2'].sum():,.0f}")
with col2:
    st.metric("Average Per Capita", f"{filtered_data['Metric Tons Per Capita'].mean():.2f}")
with col3:
    st.metric("Number of Countries", filtered_data['Country'].nunique())

# Top 10 emitting countries
st.subheader(f'Top 10 Emitting Countries in {selected_year}')
top_countries = filtered_data.groupby('Country')['Kilotons of Co2'].sum().nlargest(10)
st.bar_chart(top_countries)

# Emissions by region
st.subheader('Emissions by Region')
region_emissions = filtered_data.groupby('Region')['Kilotons of Co2'].sum().sort_values(ascending=False)
st.bar_chart(region_emissions)

# Per capita distribution
st.subheader('Per Capita Emissions Distribution')
fig, ax = plt.subplots(figsize=(10, 6))
sns.histplot(filtered_data['Metric Tons Per Capita'], bins=20, kde=True, ax=ax)
ax.set_xlabel('Metric Tons Per Capita')
ax.set_ylabel('Count')
st.pyplot(fig)

# Time series analysis
st.subheader('Global Emissions Trend')
global_trend = df.groupby('Year')['Kilotons of Co2'].sum()
st.line_chart(global_trend)

# Country comparison tool
st.subheader('Country Comparison')
selected_countries = st.multiselect('Select countries to compare', df['Country'].unique(), default=['China', 'United States', 'India'])

if selected_countries:
    country_data = df[df['Country'].isin(selected_countries)]
    fig, ax = plt.subplots(figsize=(12, 6))
    for country in selected_countries:
        country_df = country_data[country_data['Country'] == country]
        ax.plot(country_df['Year'], country_df['Kilotons of Co2'], label=country)
    ax.set_xlabel('Year')
    ax.set_ylabel('Kilotons of CO2')
    ax.set_title('CO2 Emissions Over Time')
    ax.legend()
    ax.grid(True)
    st.pyplot(fig)
