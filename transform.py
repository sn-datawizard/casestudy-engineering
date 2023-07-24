import helper
import config
import pandas as pd
import time


time.sleep(15)
start_time = time.time()
# Read data from Data Lake
conx_string = config.connection_string

population_df = pd.read_csv(f'abfs://bronze-dlscontainer-amazingetl/population.csv', storage_options = {'connection_string' : conx_string}, sep=';', index_col=False)
migration_df = pd.read_csv(f'abfs://bronze-dlscontainer-amazingetl/migration.csv', storage_options = {'connection_string' : conx_string}, sep=';', index_col=False)
birth_df = pd.read_csv(f'abfs://bronze-dlscontainer-amazingetl/birth.csv', storage_options = {'connection_string' : conx_string}, sep=';', index_col=False)

# Convert Year columns to date format YYYY-MM-DD
population_df['Year'] = pd.to_datetime(population_df['Year'].astype(str), format='%d.%m.%Y').dt.date
migration_df['Year'] = pd.to_datetime('31.12.' + migration_df['Year'].astype(str), format='%d.%m.%Y').dt.date
birth_df['YearOfBirth'] = pd.to_datetime('31.12.' + birth_df['YearOfBirth'].astype(str), format='%d.%m.%Y').dt.date

# Join dataframes
merged_df = pd.merge(population_df, birth_df, left_on='Year', right_on='YearOfBirth', how='left')
final_df = pd.merge(merged_df, migration_df, left_on='Year', right_on='Year', how='left')

# Fill NaN values with custom values
final_df['Year'].fillna('NONE', inplace=True)
final_df['Country'].fillna('NONE', inplace=True)
final_df['Immigration'].fillna(0, inplace=True)
final_df['Emigration'].fillna(0, inplace=True)
final_df['Migration'].fillna(0, inplace=True)

# Upload dataframe to Silver Data Lake
helper.upload_data(final_df, 'silver-dlscontainer-amazingetl', 'data.csv', conx_string)
time.sleep(15)

# Read csv file from Silver Data Lake
silver_df = pd.read_csv(f'abfs://silver-dlscontainer-amazingetl/data.csv', storage_options = {'connection_string' : conx_string}, sep=';', index_col=False)
#print(silver_df.head(5))

df = silver_df[['Year', 'Population']]
#print(df.head(5))

df['YoYChangePercentage'] = df['Population'].pct_change()
#print(df.head(5))

helper.upload_data(df, 'gold-dlscontainer-amazingetl', 'enriched_data.csv', conx_string)


end_time = time.time()
execution_time = end_time - start_time
print("Execution time", execution_time, "seconds")
