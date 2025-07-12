import pandas as pd
import re

def clean_player_name(name):
    if not isinstance(name,str):  # This is just for type checking 
        return None
    
    name = name.lower().strip()
    name = re.sub(r'\s+', ' ', name) # replace multiple spaces with one
    name = name.replace('.','') # replace dot in their no space
    return name

base_df = pd.read_csv('ipl.csv')
# print(base_df.head(10))


base_df.columns = ['year', 'team_name', 'player_name', 'price']
# print(perf_bat_2025_df.head(10))
column_map = {
        'StrikerName': 'player_name', 'Matches': 'matches', 'TotalRuns': 'runs', 
        'StrikeRate': 'strike_rate', 'Fours': 'fours', 'Sixes': 'sixes', 
        'HighestScore': 'highest_score'
 }

# perf_bat_2025_df = pd.read_csv('top_run_scorers_2025.csv')
# perf_bat_2025_df = perf_bat_2025_df[list(column_map.keys())].copy() # create a new data frame with only of these columns
# perf_bat_2025_df.rename(columns=column_map, inplace=True) # now only take columns which we need.
# perf_bat_2025_df['highest_score'] = pd.to_numeric(perf_bat_2025_df['highest_score'].astype(str).str.replace('*', '', regex=False), errors='coerce')
# perf_bat_2025_df['year'] = 2025
# master_df = pd.merge(base_df, perf_bat_2025_df, on=['year','player_name'], how='left')

# perf_bat_2024_df = pd.read_csv('top_run_scorers_2024.csv')
# print(perf_bat_2024_df)
# perf_bat_2024_df = perf_bat_2024_df[list(column_map.keys())].copy() # create a new data frame with only of these columns
# perf_bat_2024_df.rename(columns=column_map, inplace=True) # now only take columns which we need.
# perf_bat_2024_df['highest_score'] = pd.to_numeric(perf_bat_2024_df['highest_score'].astype(str).str.replace('*', '', regex=False), errors='coerce')
# perf_bat_2024_df['year'] = 2024
# master_df = pd.merge(master_df, perf_bat_2024_df, on=['year','player_name'], how='left')

def process_performance_data(year, column_map):
    """Process performance data for a given year"""
    try:
        df = pd.read_csv(f'top_run_scorers_{year}.csv')
        df = df[list(column_map.keys())].copy()
        df.rename(columns=column_map, inplace=True)
        df['highest_score'] = pd.to_numeric(
            df['highest_score'].astype(str).str.replace('*', '', regex=False), 
            errors='coerce'
        )
        df['year'] = year
        return df
    except FileNotFoundError:
        print(f"Warning: top_run_scorers_{year}.csv not found")
        return None

# Process multiple years
years = [2025, 2024, 2023, 2022,2021,2020,2019,2018]  
performance_dfs = []

for year in years:
    df = process_performance_data(year, column_map)
    if df is not None:
        performance_dfs.append(df)
        print(f"✅ Processed {len(df)} records for {year}")

# Combine all performance data
if performance_dfs:
    all_performance_data = pd.concat(performance_dfs, ignore_index=True)
    print(f"\nTotal performance records: {len(all_performance_data)}")
else:
    print("No performance data found!")


bowling_column_map = {
    'BowlerName': 'player_name', 'Matches': 'matches_bowled', 'Wickets': 'wickets',
    'EconomyRate': 'economy', 'OversBowled': 'overs_bowled', 'Maidens': 'maidens',
    'BBIW': 'best_bowling', 'Innings': 'innings_bowled'
}

def process_performance_data_bowling(year, column_map):
    """Process performance data for a given year"""
    try:
        df = pd.read_csv(f'most_wickets_{year}.csv')
        df = df[list(column_map.keys())].copy()
        df.rename(columns=column_map, inplace=True)
        df['year'] = year
        return df
    except FileNotFoundError:
        print(f"Warning: top_run_scorers_{year}.csv not found")
        return None

years = [2025, 2024, 2023, 2022,2021,2020,2019,2018]  
performance_dfs_bowl = []

for year in years:
    df = process_performance_data_bowling(year, bowling_column_map)
    if df is not None:
        performance_dfs_bowl.append(df)
        print(f"✅ Processed {len(df)} records for {year}")

# Combine all performance data
if performance_dfs:
    all_performance_data_bowl = pd.concat(performance_dfs_bowl, ignore_index=True)
    print(f"\nTotal performance records: {len(all_performance_data_bowl)}")
else:
    print("No performance data found!")

# all_performance_data_comp = pd.concat([all_performance_data,all_performance_data_bowl],ignore_index=True)
all_performance_data_comp = pd.merge(all_performance_data, all_performance_data_bowl, on=['year', 'player_name'], how='outer')

# Single merge with all data
master_df = pd.merge(base_df, all_performance_data_comp, on=['year', 'player_name'], how='left')
print(f"Final master dataset: {len(master_df)} records")

final_output_filename = 'ipl_master_dataset_final.csv'
master_df.sort_values(by=['year', 'price'], ascending=[False, False], inplace=True)
master_df.to_csv(final_output_filename, index=False)
