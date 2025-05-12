import pandas as pd

# Link to the file on GitHub
github_url = 'https://github.com/MyraRoseJames/Semester-Project---Hope-Foundation/raw/refs/heads/main/UNO%20Service%20Learning%20Data%20Sheet%20De-Identified%20Version.csv'

# Load the data from GitHub
data = pd.read_excel(github_url)

# Clean the data by removing rows with missing cities or states
data.dropna(subset=['Pt City', 'Pt State'], how='any', inplace=True)

# Convert necessary columns to numeric values
data['Remaining Balance'] = pd.to_numeric(data['Remaining Balance'], errors='coerce')
data['Amount'] = pd.to_numeric(data['Amount'], errors='coerce')

# Show the cleaned data
print(data.head())
