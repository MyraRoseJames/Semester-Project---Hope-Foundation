import pandas as pd

def clean_data():
    # Loading data from GitHub
    file_path = 'https://github.com/MyraRoseJames/Semester-Project---Hope-Foundation/raw/refs/heads/main/data.csv'
    data = pd.read_csv(file_path)

    # Strip extra spaces from column names
    data.columns = data.columns.str.strip()

    # Replace 'Missing' and empty strings with NaN for all columns
    data.replace({'Missing': pd.NA, '': pd.NA}, inplace=True)

    # Normalize gender values
    data['Gender'] = data['Gender'].str.strip().str.lower()  # Convert to lowercase and remove extra spaces

    # Map common variations to a single term
    gender_map = {
        'male': 'Male',
        'male ': 'Male',  # Handle any trailing spaces
        'female': 'Female',
    }

    data['Gender'] = data['Gender'].map(gender_map).fillna(data['Gender'])  # Map and fill unrecognized values

    # Convert 'Amount' to numeric (with coercion to handle any invalid values)
    data['Amount'] = pd.to_numeric(data['Amount'], errors='coerce')

    # Convert number columns to numeric (with coercion to handle invalid values)
    data['Remaining Balance'] = pd.to_numeric(data['Remaining Balance'], errors='coerce')

    # Return cleaned data
    return data
