import sys
import csv
import sqlite3
import time
import os
import psutil

class insertStationInfo:
    """
    A class to read station information from a CSV file and insert it into an SQLite database.
    It also provides methods to retrieve performance metrics like execution time and memory usage.
    """

    def __init__(self, file_name, db_name="stations.db"):
        """
        Initializes the class, setting up the file path and database connection.

        :param file_name: The path to the CSV file to be processed.
        :type file_name: str
        :param db_name: The name of the SQLite database file to use.
        :type db_name: str
        """
        self.file_name = file_name
        self.rows_in_csv = 0
        self.rows_inserted = 0
        self.runtime = 0.0
        self.mem_rss_bytes = 0
        self.mem_uss_bytes = 0
        
        # Get the process for memory profiling
        self.process = psutil.Process(os.getpid())
        
        # --- Database Setup ---
        try:
            # Connect to the SQLite database. It will be created if it doesn't exist.
            self.conn = sqlite3.connect(db_name)
            self.cursor = self.conn.cursor()
            self._create_table()
        except sqlite3.Error as e:
            print(f"Database error: {e}", file=sys.stderr)
            # In a notebook, we might not want to exit, so we raise the error
            raise

    def _create_table(self):
        """
        Creates the 'station_info' table in the database if it does not already exist.
        The table schema is designed to hold station data.

        :raises sqlite3.Error: If there is an issue creating the table.
        """
        try:
            self.cursor.execute('''
                CREATE TABLE IF NOT EXISTS station_info (
                    station_id TEXT PRIMARY KEY,
                    name TEXT NOT NULL,
                    latitude REAL,
                    longitude REAL,
                    capacity INTEGER
                )
            ''')
            self.conn.commit()
        except sqlite3.Error as e:
            print(f"Error creating table: {e}", file=sys.stderr)
            raise

    def run(self):
        """
        Executes the main logic: reading the CSV and inserting data into the database.
        This method measures the runtime and memory usage of the operation.
        """
        start_time = time.monotonic()
        
        try:
            with open(self.file_name, mode='r', encoding='utf-8') as csvfile:
                reader = csv.reader(csvfile)
                header = next(reader) # Skip header row

                for row in reader:
                    self.rows_in_csv += 1
                    try:
                        # Assumes CSV columns are in order: station_id, name, latitude, longitude, capacity
                        station_id = row[0]
                        name = row[1]
                        latitude = float(row[2])
                        longitude = float(row[3])
                        capacity = int(row[4])

                        self.cursor.execute('''
                            INSERT OR IGNORE INTO station_info (station_id, name, latitude, longitude, capacity)
                            VALUES (?, ?, ?, ?, ?)
                        ''', (station_id, name, latitude, longitude, capacity))
                        
                        # rowcount will be 1 if a row was inserted, 0 if it was ignored (due to PRIMARY KEY constraint)
                        if self.cursor.rowcount > 0:
                            self.rows_inserted += 1

                    except (ValueError, IndexError) as e:
                        print(f"Skipping malformed row {self.rows_in_csv + 1}: {row}. Error: {e}", file=sys.stderr)
                    except sqlite3.Error as e:
                        print(f"Database error on row {self.rows_in_csv + 1}: {e}", file=sys.stderr)

            self.conn.commit()

        except FileNotFoundError:
            print(f"Error: The file '{self.file_name}' was not found.", file=sys.stderr)
            return # Stop execution if file not found
        except Exception as e:
            print(f"An unexpected error occurred: {e}", file=sys.stderr)
            return
        finally:
            # Ensure the connection is closed
            if self.conn:
                self.conn.close()
        
        end_time = time.monotonic()
        self.runtime = end_time - start_time
        
        # --- Memory Measurement ---
        mem_info = self.process.memory_info()
        self.mem_rss_bytes = mem_info.rss
        # USS is not available on all platforms, handle gracefully
        try:
            self.mem_uss_bytes = self.process.memory_full_info().uss
        except (psutil.AccessDenied, AttributeError):
            self.mem_uss_bytes = 0 # USS not supported or accessible
            print("Warning: USS memory metric not available or accessible on this system.", file=sys.stderr)

    def getRows(self):
        """
        Returns the total number of data rows found in the CSV file.

        :returns: The total count of rows in the CSV.
        :rtype: int
        """
        return self.rows_in_csv

    def getRowsInserted(self):
        """
        Returns the total number of rows successfully inserted into the database.

        :returns: The total count of inserted rows.
        :rtype: int
        """
        return self.rows_inserted

    def getMemoryUSS(self):
        """
        Returns the total USS memory consumed by the program in a formatted string (MB).

        :returns: A string representing the USS memory in megabytes, or 'N/A'.
        :rtype: str
        """
        if self.mem_uss_bytes == 0:
            return "N/A"
        return f"{self.mem_uss_bytes / (1024 * 1024):.2f} MB"

    def getMemoryRSS(self):
        """
        Returns the total RSS memory consumed by the program in a formatted string (MB).

        :returns: A string representing the RSS memory in megabytes.
        :rtype: str
        """
        return f"{self.mem_rss_bytes / (1024 * 1024):.2f} MB"

    def getRuntime(self):
        """
        Returns the total time taken for the run() method in a formatted string (seconds).

        :returns: A string representing the runtime in seconds.
        :rtype: str
        """
        return f"{self.runtime:.4f} seconds"

if __name__ == "__main__":
    """
    Main execution block for command-line use.
    It expects the CSV file name as a command-line argument.
    """
    if len(sys.argv) < 2:
        print("Usage: python insertStationInfo.py <path_to_csv_file>")
        sys.exit(1)
        
    csv_file_path = sys.argv[1]

    print("Starting data insertion process from command line...")
    
    # Instantiate and run the process
    obj = insertStationInfo(file_name=csv_file_path)
    obj.run()

    # --- Output Results ---
    print("\n--- Execution Report ---")
    print(f"Total rows in CSV: {obj.getRows()}")
    print(f"Rows successfully inserted: {obj.getRowsInserted()}")
    print(f"Total Runtime: {obj.getRuntime()}")
    print(f"Memory (RSS): {obj.getMemoryRSS()}")
    print(f"Memory (USS): {obj.getMemoryUSS()}")
    print("------------------------")
    print("Process finished.")
