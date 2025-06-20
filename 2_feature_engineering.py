import pandas as pd
import numpy as np

# --- Load the cleaned census data ---
df = pd.read_csv("cleaned_census_data.csv")

# --- STEP 1: Clean column names and strip spaces ---
df.columns = df.columns.str.strip()

# --- STEP 2: Remove commas and convert to numeric early ---
for col in ['Number of Villages (Inhabited)', 'Number of Villages (Uninhabited)', 'Number of Households', 'Number of Towns']:
    df[col] = df[col].astype(str).str.replace(',', '', regex=False)
    df[col] = pd.to_numeric(df[col], errors='coerce')

# --- STEP 3: Rural-Urban Ratio using household count (better accuracy than just row count) ---
if 'Number of Households' in df.columns:
    rural_urban = df.groupby(['State Code', 'Total/Rural/Urban'])['Number of Households'].sum().unstack(fill_value=0)
    rural_urban['Rural-Urban Ratio'] = rural_urban.get('Rural', 0) / rural_urban.get('Urban', 1)
    rural_urban.reset_index(inplace=True)
    df = pd.merge(df, rural_urban[['State Code', 'Rural-Urban Ratio']], on='State Code', how='left')
else:
    print("Warning: 'Number of Households' column missing for rural-urban ratio.")

# --- STEP 4: Households per Village & per Town ---
df['Households per Village'] = np.where(
    df['Number of Villages (Inhabited)'] > 0,
    df['Number of Households'] / df['Number of Villages (Inhabited)'],
    np.nan
)

df['Households per Town'] = np.where(
    df['Number of Towns'] > 0,
    df['Number of Households'] / df['Number of Towns'],
    np.nan
)

# --- STEP 5: Uninhabited vs Inhabited Village Ratio ---
df['Uninhabited/Inhabited Ratio'] = np.where(
    df['Number of Villages (Inhabited)'] > 0,
    df['Number of Villages (Uninhabited)'] / df['Number of Villages (Inhabited)'],
    np.nan
)

# --- Final Output ---
print("Sample engineered features:")
print(df[['State Code', 'Rural-Urban Ratio', 'Households per Village', 'Households per Town', 'Uninhabited/Inhabited Ratio']].head())

# --- Save the enhanced dataset ---
df.to_csv("feature_engineered.csv", index=False)
print("\nFeature-engineered data saved as 'feature_engineered.csv'.")
