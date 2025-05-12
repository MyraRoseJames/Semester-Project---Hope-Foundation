import pandas as pd

def clean_data():
    # Loading data from GitHub
    file_path = 'https://github.com/MyraRoseJames/Semester-Project---Hope-Foundation/raw/refs/heads/main/data.csv'
    data = pd.read_csv(file_path)

    # Replace 'Missing' and empty strings with NaN for all columns
    data.replace({'Missing': pd.NA, '': pd.NA}, inplace=True)

    # Convert date columns to datetime format (with coercion to handle invalid dates)
    data['Grant Req Date'] = pd.to_datetime(data['Grant Req Date'], errors='coerce') 
    data['Payment Submitted?'] = pd.to_datetime(data['Payment Submitted?'], errors='coerce')

    # Remove rows where there is missing city and state (optional)
    # If you want to remove rows with missing city or state, you can uncomment this line
    # data.dropna(subset=['Pt City', 'Pt State'], how='any', inplace=True)

    # Convert number columns to numeric (with coercion to handle invalid values)
    data['Remaining Balance'] = pd.to_numeric(data['Remaining Balance'], errors='coerce')
    data['Amount'] = pd.to_numeric(data['Amount'], errors='coerce')

    # Return cleaned data
    return data
