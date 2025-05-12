import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Title
st.title("Data Analysis App")

# Sidebar for input selection
st.sidebar.header("Input Options")
num_rows = st.sidebar.slider("Select number of rows", 10, 100, 50)

# Create a DataFrame
data = pd.DataFrame(np.random.randn(num_rows, 3), columns=['A', 'B', 'C'])

# Show DataFrame
st.write("Here is a random DataFrame:")
st.write(data)

# Plot the data
fig, ax = plt.subplots()
data.plot(ax=ax)
st.pyplot(fig)

# Line chart for one of the columns
st.line_chart(data['A'])
