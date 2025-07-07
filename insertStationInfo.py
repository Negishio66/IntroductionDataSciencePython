import csv
import os
import sqlite3
import sys
import time
import psutil

class insertStationInfo:
    """
    Manages the process of reading a CSV file and populating a database.

    This class handles the database connection, table creation, CSV parsing,
    and data insertion. It also provides methods to retrieve performance
    and processing metrics.
    """

    def __init__(self, file_path, db_name="station_data.db"):
        """
        Initializes the insertStationInfo object.

        :param file_path: The path to the input CSV file.
        :type file_path: str
        :param db_name: The name of the SQLite database file to use.
        :type db_name: str
        """
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"The file '{file_path}' was not found.")

        self.file_path = file_path
        self.db_name = db_name
        self.conn = None
        self.process = psutil.Process(os.getpid())

        # Initialize metrics
        self._rows_in_csv = 0
        self._rows_inserted = 0
        self._runtime = 0.0
        self._memory_rss_bytes = 0
        self._memory_uss_bytes = 0

    def _connect_db(self):
        """
        Establishes a connection to the SQLite database and creates the
        'station_info' table if it doesn't already exist.
        """
        try:
            self.conn = sqlite3.connect(self.db_name)
            cursor = self.conn.cursor()
            # Create table with a schema that matches stationInfo.csv
            # Using 'IF NOT EXISTS' prevents errors on subsequent runs.
            # Using 'station_id' as PRIMARY KEY to prevent duplicates.
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS station_info (
                    station_id TEXT PRIMARY KEY,
                    name TEXT,
                    short_name TEXT,
                    lat REAL,
                    lon REAL,
                    capacity INTEGER,
                    system_id TEXT,
                    timezone TEXT,
                    rental_methods TEXT
                )
            ''')
            self.conn.commit()
        except sqlite3.Error as e:
            print(f"Database error: {e}")
            sys.exit(1)

    def run(self):
        """
        Executes the main logic: reading the CSV and inserting into the DB.

        This method orchestrates the entire process, including timing,
        memory measurement, file reading, and database insertion.
        """
        start_time = time.perf_counter()
        initial_mem_info = self.process.memory_info()

        self._connect_db()

        try:
            # Use a broader encoding in case of file variations
            with open(self.file_path, mode='r', encoding='utf-8-sig') as infile:
                reader = csv.DictReader(infile)
                data = list(reader)
                self._rows_in_csv = len(data)

                cursor = self.conn.cursor()
                for i, row in enumerate(data):
                    try:
                        lat = 0.0
                        lon = 0.0

                        # FIX: The CSV contains coordinates in a single 'Point(lon lat)' string.
                        # This logic finds that string, parses it, and extracts lat/lon.
                        # It checks common column names where this data might be.
                        point_str = next((row.get(key) for key in ['lat', 'location', 'point', 'the_geom'] if row.get(key)), None)

                        if point_str and 'Point' in point_str:
                            try:
                                # Extract numbers from 'Point(141.35 43.06)'
                                clean_str = point_str.strip().replace('Point(', '').replace(')', '')
                                coords = clean_str.split()
                                if len(coords) >= 2:
                                    lon = float(coords[0])
                                    lat = float(coords[1])
                            except (ValueError, IndexError) as parse_error:
                                print(f"Warning: Row {i + 2}: Could not parse coordinate string '{point_str}'. Error: {parse_error}")
                        
                        # Safely get and convert capacity
                        cap_val = row.get('capacity')
                        capacity = int(float(cap_val)) if cap_val and cap_val.replace('.', '', 1).isdigit() else 0

                        # Use 'INSERT OR IGNORE' to skip rows with duplicate station_id
                        cursor.execute('''
                            INSERT OR IGNORE INTO station_info (
                                station_id, name, short_name, lat, lon, capacity,
                                system_id, timezone, rental_methods
                            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                        ''', (
                            row.get('station_id'), row.get('name'), row.get('short_name'),
                            lat, lon, capacity,
                            row.get('system_id'), row.get('timezone'),
                            row.get('rental_methods')
                        ))
                        self._rows_inserted += cursor.rowcount
                    except Exception as e:
                        # Catch any other unexpected errors in a row
                        print(f"Skipping malformed row {i + 2} due to unexpected error: {e}")

            self.conn.commit()

        except IOError as e:
            print(f"Error reading file {self.file_path}: {e}")
        finally:
            if self.conn:
                self.conn.close()

        end_time = time.perf_counter()
        final_mem_info = self.process.memory_info()

        self._runtime = end_time - start_time
        self._memory_rss_bytes = final_mem_info.rss - initial_mem_info.rss
        if hasattr(final_mem_info, 'uss'):
            self._memory_uss_bytes = final_mem_info.uss - initial_mem_info.uss
        else:
            self._memory_uss_bytes = None

    def getRows(self):
        """
        Returns the total number of data rows found in the CSV file.

        :return: The count of rows in the CSV (excluding the header).
        :rtype: int
        """
        return self._rows_in_csv

    def getRowsInserted(self):
        """
        Returns the number of rows successfully inserted into the database.

        :return: The count of newly inserted rows.
        :rtype: int
        """
        return self._rows_inserted

    def getMemoryUSS(self):
        """
        Returns the Unique Set Size (USS) memory consumed by the run.

        :return: The consumed USS memory as a formatted string or 'N/A'.
        :rtype: str
        """
        if self._memory_uss_bytes is None:
            return "N/A"
        return f"{self._memory_uss_bytes / 1024**2:.2f} MB"

    def getMemoryRSS(self):
        """
        Returns the Resident Set Size (RSS) memory consumed by the run.

        :return: The consumed RSS memory as a formatted string.
        :rtype: str
        """
        return f"{self._memory_rss_bytes} Bytes"

    def getRuntime(self):
        """
        Returns the total time taken for the run() method to execute.

        :return: The total execution time as a formatted string.
        :rtype: str
        """
        return f"{self._runtime:.4f} seconds"

if __name__ == "__main__":
    """
    Main execution block to run the script from the command line.
    """
    if len(sys.argv) < 2:
        print("Usage: python insertStationInfo.py <path_to_csv_file>")
        sys.exit(1)

    file_name = sys.argv[1]

    try:
        print(f"Processing file: {file_name}")
        obj = insertStationInfo(file_name)
        obj.run()

        print("\n--- Processing Report ---")
        print(f"Total rows in CSV:     {obj.getRows()}")
        print(f"Rows inserted into DB: {obj.getRowsInserted()}")
        print(f"Total runtime:         {obj.getRuntime()}")
        print(f"Memory RSS consumed:   {obj.getMemoryRSS()}")
        print(f"Memory USS consumed:   {obj.getMemoryUSS()}")
        print("-------------------------\n")

    except FileNotFoundError as e:
        print(f"Error: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        sys.exit(1)
