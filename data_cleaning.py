import pandas as pd

def clean_data():
    # Loading data from GitHub
    file_path = 'https://github.com/MyraRoseJames/Semester-Project---Hope-Foundation/raw/refs/heads/main/data.csv'
    data = pd.read_csv(file_path)

    # Strip extra spaces from column names
    data.columns = data.columns.str.strip()

    # Replace 'Missing', 'Pending', 'Waiting on next statement', and blanks with NaN for all columns
    data.replace({'Missing': pd.NA, 'Pending': pd.NA, 'Waiting on next statement': pd.NA, '': pd.NA}, inplace=True)

    # Normalize gender values
    data['Gender'] = data['Gender'].str.strip().str.lower()  # Convert to lowercase and remove extra spaces

    # Map common variations to a single term
    gender_map = {
        'male': 'Male',
        'male ': 'Male',  # Handle any trailing spaces
        'female': 'Female',
    }

    data['Gender'] = data['Gender'].map(gender_map).fillna(data['Gender'])  # Map and fill unrecognized values

    # Clean 'Amount' column: Remove commas, '$' signs, and convert to numeric
    data['Amount'] = data['Amount'].replace({'\$': '', ',': ''}, regex=True)  # Remove $ and commas
    data['Amount'] = pd.to_numeric(data['Amount'], errors='coerce')  # Convert to numeric, coercing errors to NaN

    # Convert number columns to numeric (with coercion to handle invalid values)
    data['Remaining Balance'] = pd.to_numeric(data['Remaining Balance'], errors='coerce')

    # Convert 'Grant Req Date' to datetime format (with coercion to handle invalid dates)
    data['Grant Req Date'] = pd.to_datetime(data['Grant Req Date'], errors='coerce')

    # Handle 'Payment Submitted?' column: Create a temporary column to keep original intact
    def process_payment_date(value):
        if value == 'Yes':
            return pd.Timedelta(days=1)  # If 'Yes', treat as 1-day turnaround
        if value == 'No' or pd.isna(value):  # If 'No' or NaN, return NaT (Not a Time)
            return pd.NA
        return pd.to_datetime(value, errors='coerce')  # For valid dates, convert normally

    # Apply the process_payment_date function to create a temporary column
    data['temp_payment_submitted'] = data['Payment Submitted?'].apply(process_payment_date)

    # Now calculate the time to provide support in days
    def calculate_time_to_support(row):
        # Ensure both columns are datetime before calculation
        grant_req_date = pd.to_datetime(row['Grant Req Date'], errors='coerce')
        payment_submitted = row['temp_payment_submitte]()_
