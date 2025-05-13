import pandas as pd

# Helper function: handle Payment Submitted? values
def process_payment_date(row):
    if row['Payment Submitted?'] == 'Yes':
        return pd.Timedelta(days=1)  # 1-day turnaround
    if row['Payment Submitted?'] == 'No' or pd.isna(row['Payment Submitted?']):
        return pd.NA
    return pd.to_datetime(row['Payment Submitted?'], errors='coerce')  # Otherwise, parse date

# Helper function: calculate days from grant request to payment
def calculate_time_to_support(row):
    grant_req_date = row['Grant Req Date']
    payment_submitted = row['Payment Submitted?']

    if pd.isna(payment_submitted):
        return pd.NA
    if payment_submitted == pd.Timedelta(days=1):
        return 1
    return (payment_submitted - grant_req_date).days

# Main cleaning function
def clean_data():
    # Load data from GitHub
    file_path = 'https://github.com/MyraRoseJames/Semester-Project---Hope-Foundation/raw/refs/heads/main/data.csv'
    data = pd.read_csv(file_path)

    # Clean column names
    data.columns = data.columns.str.strip()

     # Drop empty columns 30 and 31 if they exist
    if data.shape[1] > 31:
        data.drop(data.columns[[30, 31]], axis=1, inplace=True)

    # Replace non-informative entries with NaN
    data.replace({
        'Missing': pd.NA,
        'Pending': pd.NA,
        'Waiting on next statement': pd.NA,
        '': pd.NA
    }, inplace=True)

    # Normalize and map gender values
    data['Gender'] = data['Gender'].str.strip().str.lower()
    gender_map = {
        'male': 'Male',
        'male ': 'Male',
        'female': 'Female'
    }
    data['Gender'] = data['Gender'].map(gender_map).fillna(data['Gender'])

    # Clean currency columns
    data['Amount'] = data['Amount'].replace({'\$': '', ',': ''}, regex=True)
    data['Amount'] = pd.to_numeric(data['Amount'], errors='coerce')
    data['Remaining Balance'] = pd.to_numeric(data['Remaining Balance'], errors='coerce')

    # Convert date fields
    data['Grant Req Date'] = pd.to_datetime(data['Grant Req Date'], errors='coerce')

    # Process payment dates and calculate support time
    data['Payment Submitted?'] = data.apply(process_payment_date, axis=1)
    data['time_to_support'] = data.apply(calculate_time_to_support, axis=1)

     # Save cleaned data
    data.to_csv('cleaned_data.csv', index=False)

    return data

# Run the cleaning when the file is executed directly
if __name__ == "__main__":
    clean_data()  
