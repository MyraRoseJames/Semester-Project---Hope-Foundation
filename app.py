import streamlit as st
import pandas as pd

# Load the dataset from CSV
data = pd.read_csv("data.csv")

# Display a title for your app
st.title("Hope Foundation Dashboard")
st.write("This app displays data for the Hope Foundation.")

# Show the data (first 5 rows)
st.header("Data Preview")
st.write(data.head())  # Show first 5 rows of the dataset

# Show basic data info (columns, datatypes, etc.)
st.subheader("Data Information")
st.write(data.info())
