import pandas as pd

# Sample data with junk entries
data = {
    'Name': ['John Doe', 'Jane Smith', 'NULL', 'Jake Brown', 'Ann Lee'],
    'Age': [28, None, 'NaN', 34, 'twenty-five'],
    'Email': ['john.doe@example.com', 'jane.smith@example.com', 'NULL', 'jake.brown@example.com', ''],
    'Income': ['50000', '75000', 'unknown', '60000', '70000']
}

# Load data into a DataFrame
df = pd.DataFrame(data)

# Convert columns to proper data types
df['Age'] = pd.to_numeric(df['Age'], errors='coerce')  # Convert Age to numeric, set errors to NaN
df['Income'] = pd.to_numeric(df['Income'], errors='coerce')  # Convert Income to numeric, set errors to NaN

# Drop rows with NULL or NaN in critical columns (e.g., Name, Age)
df.replace(['NULL', 'NaN', 'unknown', ''], pd.NA, inplace=True)  # Replace junk values with NaN
df.dropna(subset=['Name', 'Age', 'Email'], inplace=True)  # Drop rows with NaN in Name, Age, or Email

# Remove duplicates if any
df.drop_duplicates(inplace=True)

# Show cleaned DataFrame
print("Cleaned Data:")
print(df)
