import pandas as pd
import re
import numpy as np

# --- Step 1: Define Cleaning Functions ---

def clean_player_name(name):
    """Standardizes player names for consistent matching."""
    if not isinstance(name, str):
        return None

    # Lowercase, remove leading/trailing spaces, and collapse internal spaces
    name = name.lower().strip()
    name = re.sub(r'\s+', ' ', name) # Replace multiple spaces with a single one
    name = name.replace('.', '') # Remove dots from initials like K.L.
    return name

def parse_price(price_str):
    """Converts various price formats (e.g., '15 crore', '50,00,000') to a numeric value."""
    if pd.isna(price_str):
        return None
    
    # Convert to string and clean up
    s = str(price_str).lower().strip()
    s = s.replace(',', '').replace('â‚¹', '').replace('₹', '') # Remove commas and currency symbols
    
    try:
        # Check for 'crore'
        if 'crore' in s:
            value = float(re.search(r'(\d+\.?\d*)', s).group(1))
            return int(value * 1_00_00_000)
        # Check for 'lakh'
        elif 'lakh' in s:
            value = float(re.search(r'(\d+\.?\d*)', s).group(1))
            return int(value * 1_00_000)
        # Otherwise, assume it's a direct number
        else:
            return int(float(s))
    except (ValueError, AttributeError):
        # Return None if parsing fails
        return None

# --- Step 2: Load and Clean the First File (ipl.csv) ---
print("Processing ipl.csv...")
try:
    df1 = pd.read_csv('ipl.csv')
    
    # Standardize column names
    df1.columns = ['year', 'player_name', 'price']
    
    # Clean the data
    df1['player_name'] = df1['player_name'].apply(clean_player_name)
    df1['price_numeric'] = df1['price'].apply(parse_price)
    
    # Add a team_name column to match the structure of the second file
    df1['team_name'] = None
    
    # Select and reorder columns
    df1_cleaned = df1[['year', 'player_name', 'team_name', 'price_numeric']].copy()
    print(f"Loaded and cleaned {len(df1)} rows from ipl.csv")

except FileNotFoundError:
    print("Error: ipl.csv not found.")
    df1_cleaned = pd.DataFrame()


# --- Step 3: Load and Clean the Second File (ipl_auction_data_2018_2025.csv) ---
print("\nProcessing ipl_auction_data_2018_2025.csv...")
try:
    df2 = pd.read_csv('ipl_auction_data_2018_2025.csv')

    # Standardize column names
    df2.columns = ['player_name', 'team_name', 'price', 'year']

    # Clean the data
    df2['player_name'] = df2['player_name'].apply(clean_player_name)
    df2['team_name'] = df2['team_name'].str.strip()
    df2['price_numeric'] = df2['price'].apply(parse_price)

    # Select and reorder columns
    df2_cleaned = df2[['year', 'player_name', 'team_name', 'price_numeric']].copy()
    print(f"Loaded and cleaned {len(df2)} rows from ipl_auction_data_2018_2025.csv")

except FileNotFoundError:
    print("Error: ipl_auction_data_2018_2025.csv not found.")
    df2_cleaned = pd.DataFrame()


# --- Step 4: Combine the DataFrames ---
print("\nCombining the two datasets...")
combined_df = pd.concat([df2_cleaned, df1_cleaned], ignore_index=True)
print(f"Total rows before deduplication: {len(combined_df)}")

# Drop rows where player name or price is invalid
combined_df.dropna(subset=['player_name', 'price_numeric'], inplace=True)
combined_df = combined_df[combined_df['player_name'] != '']
print(f"Rows after dropping invalid entries: {len(combined_df)}")


# --- Step 5: Handle Duplicates ---
# Sort by team_name so that rows with a team name are prioritized when dropping duplicates
# (NaNs are sorted to the end, so we keep the first non-NaN entry)
combined_df['team_name_is_null'] = combined_df['team_name'].isnull()
combined_df.sort_values(by=['player_name', 'year', 'team_name_is_null'], inplace=True)

# Drop duplicates based on player and year, keeping the first (and hopefully most complete) entry
merged_df = combined_df.drop_duplicates(subset=['player_name', 'year'], keep='first')

# Clean up final DataFrame
merged_df = merged_df.drop(columns=['team_name_is_null'])
merged_df = merged_df.sort_values(by=['year', 'price_numeric'], ascending=[False, False]).reset_index(drop=True)
# Convert price to integer
merged_df['price_numeric'] = merged_df['price_numeric'].astype(int)

print(f"Total rows after deduplication: {len(merged_df)}")


# --- Step 6: Save the Final Merged File ---
output_filename = 'ipl_auction_data_merged_2018-2025.csv'
merged_df.to_csv(output_filename, index=False)

print(f"\nSuccessfully merged the data and saved to '{output_filename}'")
print("\n--- First 10 rows of the final merged data ---")
print(merged_df.head(10))
print("\n--- Data Info ---")
merged_df.info()

print(merged_df.head())


