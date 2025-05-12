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
    data['Gender'] = data['Gender'].str.strip().str.lower()

    # Map common variations to a single term
    gender_map = {
        'male': 'Male',
        'male ': 'Male',
        'female': 'Female'
    }
    data['Gender'] = data['Gender'].map(gender_map).fillna(data['Gender'])

    # Create a clean numeric version of 'Amount' without overwriting the original
    data['Amount_clean'] = data['Amount'].replace({
        'Missing': pd.NA,
        'Pending': pd.NA,
        'Waiting on next statement': pd.NA,
        '': pd.NA
    })
    data['Amount_clean'] = data['Amount_clean'].replace({'\$': '', ',': ''}, regex=True)
    data['Amount_clean'] = pd.to_numeric(data['Amount_clean'], errors='coerce')

    # Convert number columns to numeric
    data['Remaining Balance'] = pd.to_numeric(data['Remaining Balance'], errors='coerce')
    data['Remaining_Balance_clean'] = data['Remaining Balance']  # Optional: create a cleaned version if needed

    # Convert 'Grant Req Date' to datetime
    data['Grant Req Date'] = pd.to_datetime(data['Grant Req Date'], errors='coerce')

    # Handle 'Payment Submitted?' column
    def process_payment_date(row):
        if row['Payment Submitted?'] == 'Yes':
            return pd.Timedelta(days=1)
        if row['Payment Submitted?'] == 'No' or pd.isna(row['Payment Submitted?']):
            return pd.NA
        return pd.to_datetime(row['Payment Submitted?'], errors='coerce')

    data['Payment Submitted?'] = data.apply(process_payment_date, axis=1)

    # Calculate time to provide support
    def calculate_time_to_support(row):
        grant_req_date = pd.to_datetime(row['Grant Req Date'], errors='coerce')
        payment_submitted =_
