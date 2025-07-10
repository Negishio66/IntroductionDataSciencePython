import pandas as pd
import psycopg2
from psycopg2 import sql
import os

# --- 1. Database Connection Configuration ---
# Please configure the following dictionary with your database connection details.
# It is recommended to use environment variables for sensitive data in production.
DB_CONFIG = {
    "dbname": "s1282009",
    "user": "s1282009",
    "password": "6thStationPiano",
    "host": "localhost",  # e.g., 'localhost' or an IP address
    "port": "5432"      # The default PostgreSQL port
}

# The path to the folder containing the station information CSV file.
DATA_DIRECTORY = '~' 
# The filename for the station information CSV.
STATION_INFO_FILENAME = 'stationInfo.csv'
# The name of the data table in the PostgreSQL database.
DATA_TABLE = "data"
# The desired name for the final, processed output file.
OUTPUT_FILENAME = "pm25_by_station_final.csv"

print("Initiating data processing script...")

try:
    # --- 2. Load Station Information from CSV ---
    station_info_path = os.path.join(DATA_DIRECTORY, STATION_INFO_FILENAME)
    print(f"Loading station information from: {station_info_path}")
    
    # Read the station information CSV file into a pandas DataFrame.
    # The 'stationId' is specified as a string to prevent data type issues.
    station_df = pd.read_csv(station_info_path, dtype={'stationId': str})
    
    # Parse the 'Location' column to extract longitude and latitude coordinates.
    print("Parsing coordinates from 'Location' column...")
    coords = station_df['Location'].str.extract(r'Point\(([\d\.]+) ([\d\.]+)\)')
    station_df['longitude'] = coords[0]
    station_df['latitude'] = coords[1]
    
    # Rename the 'stationId' column to 'stationID' to ensure consistency
    # with the 'Data' table schema for a successful merge operation.
    station_df.rename(columns={'stationId': 'stationid'}, inplace=True)
    print("Successfully loaded and parsed station information.")

    # --- 3. Retrieve Sensor Data from PostgreSQL ---
    print("Connecting to PostgreSQL to retrieve sensor data...")
    query = sql.SQL('SELECT "stationid", "obsdate", "pm25" FROM {}').format(
        sql.Identifier(DATA_TABLE)
    )
    
    with psycopg2.connect(**DB_CONFIG) as conn:
        print("Executing database query...")
        # Load data directly into a DataFrame, parsing the date column appropriately.
        data_df = pd.read_sql_query(query.as_string(conn), conn, parse_dates=['obsdate'])
        print(f"Successfully retrieved {len(data_df)} records from the '{DATA_TABLE}' table.")

    # --- 4. Merge the two DataFrames ---
    print("Merging data from the CSV file and the database...")
    # This operation combines the two data sources using the common 'stationID' column.
    merged_df = pd.merge(data_df, station_df, on='stationid')

    # --- 5. Create the 'Point(x, y)' Identifier and Pivot ---
    print("Constructing 'Point(x, y)' identifier and pivoting data...")
    # Create a new column for the pivot operation headers.
    merged_df['point_header'] = (
        'Point(' + merged_df['longitude'].astype(str) + 
        ' ' + merged_df['latitude'].astype(str) + ')'
    )
    
    # Reshape the data to have timestamps as rows and station points as columns.
    pivoted_df = merged_df.pivot_table(
        index='obsdate',
        columns='point_header',
        values='pm25'
    )

    # --- 6. Format and Export to CSV ---
    # Set the name for the index column for clarity in the final CSV.
    pivoted_df.index.name = 'TimeStamp'
    # Remove the name of the column index for a cleaner header.
    pivoted_df.columns.name = None

    output_path = os.path.join(DATA_DIRECTORY, OUTPUT_FILENAME)
    print(f"Writing the final transformed data to: {output_path}")
    pivoted_df.to_csv(output_path)

    print(f"\nProcess complete. The output has been saved to '{OUTPUT_FILENAME}'.")

except FileNotFoundError:
    print(f"\nError: The station information file could not be found. Please ensure '{STATION_INFO_FILENAME}' is located in the directory: '{DATA_DIRECTORY}'.")
except psycopg2.OperationalError as e:
    print(f"\nError: Could not connect to the database. Please verify the connection details in DB_CONFIG. Details: {e}")
except Exception as e:
    print(f"\nAn unexpected error occurred during script execution. Details: {e}")