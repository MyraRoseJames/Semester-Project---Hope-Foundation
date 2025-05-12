import pandas as pd

# Loading data from Github
file_path = 'https://github.com/MyraRoseJames/Semester-Project---Hope-Foundation/raw/refs/heads/main/data.csv'
data = pd.read_csv(file_path)

# decided to replace both missing and blanks with NaN for all columns
data.replace('Missing', pd.NA, inplace=True)
data.replace('', pd.NA, inplace=True)

# Convert the two columns with dates to date time format
# coerce needed to onvert date columns, set invalid data to NaT
data['Grant Req Date'] = pd.to_datetime(data['Grant Req Date'], errors='coerce') 
data['Payment Submitted?'] = pd.to_datetime(data['Payment Submitted?'], errors='coerce')

# Remove rows where there is missing city and state, or city or state WILL PROBABLY NOT DO THIS DEPENDING ON HOW MANY
#data.dropna(subset=['Pt City', 'Pt State'], how='any', inplace=True)

#number consistancy
data['Remaining Balance'] = pd.to_numeric(data['Remaining Balance'], errors='coerce')
data['Amount'] = pd.to_numeric(data['Amount'], errors='coerce')

# After cleaning, inspect the first few rows to ensure the changes were applied correctly
data.head()
