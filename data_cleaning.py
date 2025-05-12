import pandas as pd

def clean_data():
    # Loading data from GitHub
    file_path = 'https://github.com/MyraRoseJames/Semester-Project---Hope-Foundation/raw/refs/heads/main/data.csv'
    data = pd.read_csv(file_path)

    # Strip extra spaces from column names
    data.columns = data.columns.str.strip()

    # Replace 'Missing', 'Pending', 'Waiting on next statement', and blanks with NaN for all columns
    data.replace({
        'Missing': pd.NA,
        'Pending': pd.NA,
        'Waiting on next statement': pd.NA,
        '': pd.NA
    }, inplace=True)

    # Normalize gender values
    data['Gender'] = data['Gender'].str.strip().str.lower()  # Convert to lowercase and remove extra spaces

    # Map common variations to a single term
    gender_map = {
        'male': 'Male',
        'male ': 'Male',  # Handle any trailing spaces
        'female': 'Female'
    }
    
    data['Gender'] = data['Gender'].map(gender_map).fillna(data['Gender'])  # Map and fill unrecognized values

    # Clean 'Amount' column: Remove commas, '$' signs, and convert to numeric
    data['Amount'] = data['Amount'].replace({'\$': '', ',': ''}, regex=True)  # Remove $ and commas
    data['Amount'] = pd.to_numeric(data['Amount'], errors='coerce')  # Convert to numeric, coercing errors to NaN

    # Convert number columns to numeric (with coercion to handle invalid values)
    data['Remaining Balance'] = pd.to_numeric(data['Remaining Balance'], errors='coerce')

    # Convert 'Grant Req Date' to datetime format (with coercion to handle invalid dates)
    data['Grant Req Date'] = pd.to_datetime(data['Grant Req Date'], errors='coerce')

    # Handle 'Payment Submitted?' column:
    # If 'Yes', set 1-day turnaround; else, coerce to datetime
    def process_payment_date(row):
        if row['Payment Submitted?'] == 'Yes':
            return pd.Timedelta(days=1)  # If 'Yes', treat as 1-day turnaround
        if row['Payment Submitted?'] == 'No' or pd.isna(row['Payment Submitted?']):
            return pd.NA  # If 'No' or NaN, return NaT (Not a Time)
        return pd.to_datetime(row['Payment Submitted?'], errors='coerce')  # For dates, convert normally

    data['Payment Submitted?'] = data.apply(process_payment_date, axis=1)

    # Now calculate the time to provide support in days
    def calculate_time_to_support(row):
        # Ensure both columns are datetime before calculation
        grant_req_date = pd.to_datetime(row['Grant Req Date'], errors='coerce')
        payment_submitted = pd.to_datetime(row['Payment Submitted?'], errors='coerce')

        # If payment is missing or 'No', return NaT
        if pd.isna(payment_submitted) or payment_submitted == pd.NaT:
            return pd.NA
        # If 'Yes', return 1 day turnaround
        if payment_submitted == pd.Timedelta(days=1):
            return 1
        # Calculate the days difference
        return (payment_submitted - grant_req_date).days

    # Apply function to calculate time_to_support
    data['time_to_support'] = data.apply(calculate_time_to_support, axis=1)

    # Return cleaned data
    return data
