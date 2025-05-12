import pandas as pd

# Link to the file on GitHub
github_url = 'https://raw.githubusercontent.com/MyraRoseJames/Semester-Project---Hope-Foundation/raw/refs/heads/main/NCSHF_Patient%20Assistance%20Dataset_Info%20for%20UNO%20SLA.xlsx'

# Load the data from GitHub
data = pd.read_excel(github_url)

# Clean the data by removing rows with missing cities or states
data.dropna(subset=['Pt City', 'Pt State'], how='any', inplace=True)

# Convert necessary columns to numeric values
data['Remaining Balance'] = pd.to_numeric(data['Remaining Balance'], errors='coerce')
data['Amount'] = pd.to_numeric(data['Amount'], errors='coerce')

# Show the cleaned data
print(data.head())
