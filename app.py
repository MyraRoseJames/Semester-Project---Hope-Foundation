import pandas as pd
import streamlit as st
from data_cleaning import clean_data  # Import the cleaning function

# Clean data
cleaned_data = clean_data()

# Sidebar navigation
st.sidebar.title("Navigation")
page = st.sidebar.radio("Select a page:", ["Data Preview", "Applications Ready for Review", "Support Breakdown", "Time to Provide Support", "Unused Grant Amounts", "Summary of Impact and Progress"])

# Display the page based on selection
if page == "Data Preview":
    st.title("Hope Foundation Dashboard")
    st.write("Cleaned data for the Hope Foundation")
    st.header("Data Preview")
    st.write(cleaned_data.head())  # Show the cleaned data

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

    # Create a temporary copy of 'Payment Submitted?' column for time calculations
    cleaned_data['temp_payment_submitted'] = cleaned_data['Payment Submitted?']

    # Convert 'Grant Req Date' and 'temp_payment_submitted' to datetime (coerce invalid dates to NaT)
    cleaned_data['Grant Req Date'] = pd.to_datetime(cleaned_data['Grant Req Date'], errors='coerce')
    cleaned_data['temp_payment_submitted'] = pd.to_datetime(cleaned_data['temp_payment_submitted'], errors='coerce')

    # Handle 'temp_payment_submitted' column: 'Yes' = 1-day turnaround, else NaT for invalid entries
    def process_payment_date(row):
        if row['temp_payment_submitted'] == 'Yes':
            return pd.Timedelta(days=1)  # If 'Yes', treat as 1-day turnaround
        if row['temp_payment_submitted'] == 'No' or pd.isna(row['temp_payment_submitted']):
            return pd.NA  # If 'No' or NaN, return NaT (Not a Time)
        return row['temp_payment_submitted']  # For valid dates, return as is

    # Apply the processing logic to the 'temp_payment_submitted' column
    cleaned_data['temp_payment_submitted'] = cleaned_data.apply(process_payment_date, axis=1)

    # Now calculate the time to provide support in days
    def calculate_time_to_support(row):
        # If 'temp_payment_submitted' is NaT or 'No', return NaT
        if pd.isna(row['temp_payment_submitted']):
            return pd.NaT
        # If 'Yes', return 1 day turnaround
        if row['temp_payment_submitted'] == pd.Timedelta(days=1):
            return 1
        # Calculate the days difference
        return (row['temp_payment_submitted'] - row['Grant Req Date']).days

    # Apply the time calculation
    cleaned_data['time_to_support'] = cleaned_data.apply(calculate_time_to_support, axis=1)

    # Calculate average time to provide support (ignoring NaT)
    avg_time = cleaned_data['time_to_support'].mean()

    # Display the average time
    st.write(f"Average time to provide support: {avg_time:.2f} days")

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
    avg_support_time = cleaned_data["time_to_support"].mean()

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

