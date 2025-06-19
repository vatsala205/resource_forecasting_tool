import pandas as pd

# Load the CSV
df = pd.read_csv("census_data.csv", encoding="utf-8-sig")

# Clean numeric fields
num_cols = ['Population (Persons)', 'Population (Males)', 'Population (Females)', 'Population Density']
for col in num_cols:
    df[col] = df[col].astype(str).str.replace(',', '').str.strip().replace('', '0').astype(float)

# Convert codes to numeric
df['District Code'] = pd.to_numeric(df['District Code'], errors='coerce')
df['Sub District Code'] = pd.to_numeric(df['Sub District Code'], errors='coerce')

# Drop rows with critical missing values
df.dropna(subset=['Area (sq km)', 'Population Density'], inplace=True)

# Save cleaned version
df.to_csv("cleaned_census_data.csv", index=False)


print("Cleaned data saved. Sample rows:")
print(df.head())
print(df.dtypes)