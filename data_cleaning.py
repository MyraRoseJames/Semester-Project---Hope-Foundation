import pandas as pd

from datetime import datetime

# Helper function: handle Payment Submitted? values
def process_payment_date(row):
    if row['Payment Submitted?'] == 'Yes':
        return pd.Timedelta(days=1)  # 1-day turnaround
    if row['Payment Submitted?'] == 'No' or pd.isna(row['Payment Submitted?']):
        return pd.NA
    return pd.to_datetime(row['Payment Submitted?'], errors='coerce')  # Otherwise, parse date

# Helper function: calculate days from grant request to payment
def calculate_days_to_support(row):
    grant_req_date = row['Grant Req Date']
    parsed_payment = row['_parsed_payment_date']

    if pd.isna(parsed_payment):
        return pd.NA
    if parsed_payment == pd.Timedelta(days=1):
        return 1
    return (parsed_payment - grant_req_date).days

# Main cleaning function
def clean_data():
    # Load data from GitHub
    file_path = 'https://github.com/MyraRoseJames/Semester-Project---Hope-Foundation/raw/refs/heads/main/data.csv'
    data = pd.read_csv(file_path)

    # Clean column names
    data.columns = data.columns.str.strip()

    # Clean and standardize Insurance Type
    if 'Insurance Type' in data.columns:
        data['Insurance Type'] = data['Insurance Type'].astype(str).str.strip().str.title()
    
        insurance_corrections = {
            'Uninsurred': 'Uninsured',
            'Unisured': 'Uninsured',
            'Medicaid & Medicare': 'Medicare & Medicaid',
            'MediCare': 'Medicare',
            'MEdicare': 'Medicare',
            'Medicaid ': 'Medicaid',
            'Medicare ': 'Medicare',
            'Private ': 'Private',
            'Uninsured ': 'Uninsured',
            'Healthcare.Gov': 'Healthcare.gov',
            'Heathcare.Gov': 'Healthcare.gov',
            'Missing': 'Unknown',
            '': 'Unknown'
        }

    data['Insurance Type'] = data['Insurance Type'].replace(insurance_corrections)

    data['Insurance Type'] = data['Insurance Type'].fillna('Unknown') #for the missing values

    # Clean and bin 'Total Household Gross Monthly Income'
    if 'Total Household Gross Monthly Income' in data.columns:
        # Convert to numeric
        data['Total Household Gross Monthly Income'] = (
            data['Total Household Gross Monthly Income']
            .replace('[\$,]', '', regex=True)
            .replace('', pd.NA)
        )
        data['Total Household Gross Monthly Income'] = pd.to_numeric(
            data['Total Household Gross Monthly Income'], errors='coerce'
        )

        # Define income bins and labels
        income_bins = [0, 2000, 4000, 6000, 8000, float('inf')]
        income_labels = ['< $2,000', '$2,000–3,999', '$4,000–5,999', '$6,000–7,999', '$8,000+']

        # Bin numeric values into ranges
        data['Income Range'] = pd.cut(
            data['Total Household Gross Monthly Income'],
            bins=income_bins,
            labels=income_labels
        )

        # Add 'Missing' as a category for NaN values
        data['Income Range'] = data['Income Range'].astype(object)
        data.loc[data['Total Household Gross Monthly Income'].isna(), 'Income Range'] = 'Missing'

    # Calculate Age from DOB
    if 'DOB' in data.columns:
        data['DOB'] = pd.to_datetime(data['DOB'], errors='coerce')
        today = pd.to_datetime(datetime.today().date())
        data['Age'] = (today - data['DOB']).dt.days // 365


    # Drop empty columns 30 and 31 if they exist
    if data.shape[1] > 31:
        data.drop(data.columns[[30, 31]], axis=1, inplace=True)

    if 'Pt City' in data.columns:
        # Keep missing values as NaN instead of converting to string 'nan'
        data['Pt City'] = data['Pt City'].where(data['Pt City'].notna())
        data['Pt City'] = data['Pt City'].str.strip().str.title()
    
    city_corrections = {
        'Omahaa': 'Omaha',
        'Omaha,': 'Omaha',
        'Omha': 'Omaha',
        'OmAha': 'Omaha',
        'O maha': 'Omaha',
        'Lincon': 'Lincoln',
    }

    data['Pt City'] = data['Pt City'].replace(city_corrections)

    # Replace non-informative entries with NaN
    data.replace({
        'Missing': pd.NA,
        #'Pending': pd.NA, took out later, need for ready to review
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

    # Create a new temporary column with parsed dates for calculation
    data['_parsed_payment_date'] = data.apply(process_payment_date, axis=1)

    # Compute days to support
    data['days_to_support'] = data.apply(calculate_days_to_support, axis=1)

    # Drop the temporary column
    data.drop(columns=['_parsed_payment_date'], inplace=True)

    # Save cleaned data
    data.to_csv('cleaned_data.csv', index=False)

    return data

# Run the cleaning when the file is executed directly
if __name__ == "__main__":
    clean_data()
