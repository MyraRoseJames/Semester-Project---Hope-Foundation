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
    st.title("Support Breakdown")

    # Ensure Amount is numeric
    cleaned_data['Amount'] = pd.to_numeric(cleaned_data['Amount'], errors='coerce')

    # Set up tabs for each demographic
    gender_tab, location_tab, income_tab, insurance_tab, age_tab = st.tabs([
        "By Gender", "By Location", "By Income Size", "By Insurance Type", "By Age"
    ])

    with gender_tab:
        st.subheader("Support by Gender")
        support_by_gender = cleaned_data.groupby('Gender')['Amount'].sum().sort_values(ascending=False)
        support_by_gender = support_by_gender.apply(lambda x: f"${x:,.2f}")
        st.write(support_by_gender)

    with location_tab:
        st.subheader("Support by Location (Pt City)")
        support_by_city = cleaned_data.groupby('Pt City')['Amount'].sum().sort_values(ascending=False)
        support_by_city = support_by_city.apply(lambda x: f"${x:,.2f}")
        st.write(support_by_city)

    with income_tab:
        st.subheader("Support by Income Range (including missing)")

        if 'Income Range' in cleaned_data.columns:
            support_by_income_range = (
                cleaned_data.groupby('Income Range')['Amount']
                .sum()
                .reindex(['< $2,000', '$2,000–3,999', '$4,000–5,999', '$6,000–7,999', '$8,000+', 'Missing'])
            )
            support_by_income_range = support_by_income_range.fillna(0).apply(lambda x: f"${x:,.2f}")
            st.write(support_by_income_range)
        else:
            st.warning("Income Range column not found.")

    with insurance_tab:
        st.subheader("Support by Insurance Type")
        if 'Insurance Type' in cleaned_data.columns:
            support_by_insurance = cleaned_data.groupby('Insurance Type')['Amount'].sum().sort_values(ascending=False)
            support_by_insurance = support_by_insurance.apply(lambda x: f"${x:,.2f}")
            st.write(support_by_insurance)

    with age_tab:
        st.subheader("Support by Age Group")
        if 'Age' in cleaned_data.columns:
            # Optional: bin ages into groups
            cleaned_data['Age Group'] = pd.cut(cleaned_data['Age'], bins=[0, 18, 30, 45, 60, 100], labels=[
                '0–18', '19–30', '31–45', '46–60', '60+'])
            support_by_age = cleaned_data.groupby('Age Group')['Amount'].sum().sort_values(ascending=False)
            support_by_age = support_by_age.apply(lambda x: f"${x:,.2f}")
            st.write(support_by_age)

elif page == "Time to Provide Support":
    st.title("Time to Provide Support")

    support_data = cleaned_data.dropna(subset=['days_to_support', 'Grant Req Date'])

    # Extract year and month from grant request date
    support_data['Request Year'] = support_data['Grant Req Date'].dt.year
    support_data['Request Month'] = support_data['Grant Req Date'].dt.strftime('%Y-%m')

    # Average time overall
    avg_time = support_data['days_to_support'].mean()
    st.metric("Average Time to Provide Support", f"{avg_time:.2f} days")

    # Grouped averages
    avg_by_year = support_data.groupby('Request Year')['days_to_support'].mean().reset_index()
    avg_by_month = support_data.groupby('Request Month')['days_to_support'].mean().reset_index()

    # Charts
    fig_year = px.line(
        avg_by_year,
        x='Request Year',
        y='days_to_support',
        title='Yearly Support Time',
        markers=True,
        labels={'days_to_support': 'Avg Days to Support'}
    )

    fig_month = px.line(
        avg_by_month,
        x='Request Month',
        y='days_to_support',
        title='Monthly Support Time',
        markers=True,
        labels={'days_to_support': 'Avg Days to Support'}
    )

    # 🔀 Add tabs
    tab1, tab2 = st.tabs(["By Year", "By Month"])

    with tab1:
        st.subheader("Average Time to Support by Year")
        st.plotly_chart(fig_year, use_container_width=True)

    with tab2:
        st.subheader("Average Time to Support by Month")
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

