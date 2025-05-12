import streamlit as st
from data_cleaning import clean_data  # Import the cleaning function

# Clean data
cleaned_data = clean_data()

# Sidebar navigation
st.sidebar.title("Navigation")
page = st.sidebar.radio("Select a page:", ["Data Preview", "Applications Ready for Review", "Support Breakdown", "Time to Provide Support", "Unused Grant Amounts"])

# Display the page based on selection
if page == "Data Preview":
    st.title("Hope Foundation Dashboard")
    st.write("This app displays cleaned data for the Hope Foundation.")
    st.header("Data Preview")
    st.write(cleaned_data.head())  # Show the cleaned data

elif page == "Applications Ready for Review":
    st.title("Applications Ready for Review")
    # Assuming a column called 'signed' to filter applications (True or False)
    ready_for_review = cleaned_data[cleaned_data['signed'] == True]
    st.write(ready_for_review)

elif page == "Support Breakdown":
    st.title("Support Breakdown by Demographics")
    # You can modify this part to show breakdowns like gender, location, etc.
    support_by_gender = cleaned_data.groupby('gender')['support_amount'].sum()
    st.write(support_by_gender)

elif page == "Time to Provide Support":
    st.title("Time to Provide Support")
    # Assuming there's a column for request date and support date
    cleaned_data['time_to_support'] = pd.to_datetime(cleaned_data['Payment Submitted?']) - pd.to_datetime(cleaned_data['Grant Req Date'])
    avg_time = cleaned_data['time_to_support'].mean()
    st.write(f"Average time to provide support: {avg_time.days} days")

elif page == "Unused Grant Amounts":
    st.title("Unused Grant Amounts")
    # Assuming there's a column 'Amount' and 'Remaining Balance'
    unused_grants = cleaned_data[cleaned_data['Amount'] > cleaned_data['Remaining Balance']]
    avg_unused = unused_grants['Amount'] - unused_grants['Remaining Balance']
    st.write(f"Total unused grants: {unused_grants.shape[0]}")
    st.write(f"Average unused amount: {avg_unused.mean()}")
