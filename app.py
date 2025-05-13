import streamlit as st
import pandas as pd
import plotly.express as px
from data_cleaning import clean_data

# Clean data
cleaned_data = clean_data()

# Sidebar navigation
st.sidebar.title("Navigation")
page = st.sidebar.radio("Select a page:", ["Data Preview", "Applications Ready for Review", "Support Breakdown", "Time to Provide Support", "Unused Grant Amounts", "Summary of Impact and Progress"])

if page == "Data Preview":
    st.title("Hope Foundation Dashboard")
    st.subheader("Cleaned Data Preview")

    # Show shape and column names
    st.markdown(f"**Dataset shape:** {cleaned_data.shape[0]} rows × {cleaned_data.shape[1]} columns")
    st.markdown("**Column names:**")
    st.write(cleaned_data.columns.tolist())

    # Show sample of the data
    st.subheader("Sample of Cleaned Data")
    st.dataframe(cleaned_data.head(10))

    # Null value count
    st.subheader("Missing Values by Column")
    st.dataframe(cleaned_data.isnull().sum().reset_index().rename(columns={
        'index': 'Column', 0: 'Missing Values'
    }))

    # Data types
    st.subheader("Column Data Types")
    st.dataframe(cleaned_data.dtypes.reset_index().rename(columns={
        'index': 'Column', 0: 'Data Type'
    }))

elif page == "Data Information":
    st.title("Data Information")
    st.subheader("Detailed Data Info")
    st.write("This section shows the data types and number of non-null values.")
    # Show data info with more detailed information about column types
    st.write(cleaned_data.info(verbose=True))  # Show more detailed info
    st.write("Data Types per Column:")
    st.write(cleaned_data.dtypes)  # Show data types for each column

elif page == "Applications Ready for Review":
    st.title("Applications Ready for Review")
    # Assuming a column called 'signed' to filter applications (True or False)
    ready_for_review = cleaned_data[cleaned_data['Application Signed?'] == 'Yes']
    st.write(ready_for_review)

elif page == "Support Breakdown":
    st.title("Support Breakdown by Demographics")

    # Group by 'Gender' and calculate the total 'Amount'
    support_by_gender = cleaned_data.groupby('Gender')['Amount'].sum()

    # Format the 'Amount' to include commas and dollar signs
    support_by_gender = support_by_gender.apply(lambda x: f"${x:,.2f}")  # Format with commas and dollar sign

    # Display the formatted support breakdown
    st.write(support_by_gender)

elif page == "Time to Provide Support":
    st.title("Time to Provide Support")

    # Filter for rows with valid support times and request dates
    support_data = cleaned_data.dropna(subset=['days_to_support', 'Grant Req Date'])

    # Extract year and month from the grant request date
    support_data['Request Year'] = support_data['Grant Req Date'].dt.year
    support_data['Request Month'] = support_data['Grant Req Date'].dt.strftime('%Y-%m')

    # Overall average support time
    avg_time = support_data['days_to_support'].mean()
    st.metric("Average Time to Provide Support", f"{avg_time:.2f} days")

    # Group by year
    avg_by_year = support_data.groupby('Request Year')['days_to_support'].mean().reset_index()

    # Group by month
    avg_by_month = support_data.groupby('Request Month')['days_to_support'].mean().reset_index()

    # Plot: Yearly average
    fig_year = px.line(
        avg_by_year,
        x='Request Year',
        y='days_to_support',
        title='Average Time to Provide Support by Year',
        markers=True,
        labels={'days_to_support': 'Avg Days to Support'}
    )
    st.plotly_chart(fig_year, use_container_width=True)

    # Plot: Monthly average
    fig_month = px.line(
        avg_by_month,
        x='Request Month',
        y='days_to_support',
        title='Average Time to Provide Support by Month',
        markers=True,
        labels={'days_to_support': 'Avg Days to Support'}
    )
    st.plotly_chart(fig_month, use_container_width=True)

elif page == "Unused Grant Amounts":
    st.title("Unused Grant Amounts")

    # Drop rows with missing values in Amount or Remaining Balance
    unused_data = cleaned_data.dropna(subset=["Amount", "Remaining Balance"])

    # Filter where Remaining Balance > 0
    unused_grants = unused_data[unused_data["Remaining Balance"] > 0]

     # Count and percentage
    num_unused = len(unused_grants)
    total = len(unused_data)
    percent_unused = (num_unused / total) * 100 if total > 0 else 0

    # Average remaining
    avg_remaining = unused_grants["Remaining Balance"].mean()

    # Display metrics
    st.metric("Total Applications with Unused Grants", f"{num_unused}")
    st.metric("Percentage of Grants Unused", f"{percent_unused:.2f}%")
    st.metric("Average Remaining Balance", f"${avg_remaining:,.2f}")

    # Show details
    st.subheader("Details of Unused Grants")
    st.dataframe(unused_grants[["Amount", "Remaining Balance", "Gender", "Pt City", "Insurance Type"]])

elif page == "Summary of Impact and Progress":
    st.title("Summary of Impact and Progress")
    st.subheader("Key Insights from the Past Year")

    # Total number of applications
    total_apps = len(cleaned_data)

    # Total amount distributed
    total_distributed = cleaned_data["Amount"].sum()

    # Average amount awarded (non-null values only)
    avg_award = cleaned_data["Amount"].mean()

    # Average time to provide support (calculated in your data_cleaning.py)
    avg_support_time = cleaned_data["days_to_support"].mean()

    # Number of unique cities served
    num_cities = cleaned_data["Pt City"].nunique()

    # Metrics row
    col1, col2, col3 = st.columns(3)
    col1.metric("Total Applications", f"{total_apps}")
    col2.metric("Total Amount Distributed", f"${total_distributed:,.2f}")
    col3.metric("Average Award Amount", f"${avg_award:,.2f}")

    col4, col5 = st.columns(2)
    col4.metric("Avg. Days to Support", f"{avg_support_time:.2f} days" if avg_support_time else "N/A")
    col5.metric("Cities Served", f"{num_cities}")

    # Optional: Gender breakdown
    st.subheader("Support by Gender")
    gender_counts = cleaned_data["Gender"].value_counts(dropna=False)
    st.bar_chart(gender_counts)

    # Optional: Top cities served
    st.subheader("Top 5 Cities by Number of Applications")
    top_cities = cleaned_data["Pt City"].value_counts().head(5)
    st.bar_chart(top_cities)

