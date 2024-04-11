import sqlite3
from pathlib import Path

DB_FILE = Path("./data.db")
TABLE = 'events'
BAND = 'Lions'
DATE = '2088.10.15'
BANDS_DATA = [
    ("Wolves", "Wolf City", "2088.11.15"),
    ("Leopards", "Leopard City", "2088.11.15"),
    ("Snakes", "Snake City", "2088.11.25")
]


def fetch_band_data(this_band=None, this_date=None):    
    connection = sqlite3.connect(DB_FILE)
    cursor = connection.cursor()
    
    # Execute SQL query based on provided band name or date
    if this_band:
        cursor.execute(f"SELECT * FROM {TABLE} WHERE band = ?", (this_band,))
    elif this_date:
        cursor.execute(f"SELECT * FROM {TABLE} WHERE date = ?", (this_date,))
    
    # Fetch all matching rows
    rows = cursor.fetchall()  # returns list of tuples (rows)    
    connection.close()  # Close the database connection
    
    return rows

def fetch_all_bands_data():
    connection = sqlite3.connect(DB_FILE)
    cursor = connection.cursor()
    
    # Execute SQL query to fetch all rows
    cursor.execute(f"SELECT * FROM {TABLE}")   
    
    rows = cursor.fetchall()  # Fetch all rows    
    connection.close()  # Close the database connection
    
    return rows

def insert_one_band(one_band_row):
    connection = sqlite3.connect(DB_FILE)
    cursor = connection.cursor()
    
    # Execute SQL query to insert one row
    cursor.execute(f"INSERT INTO {TABLE} VALUES(?,?,?)", one_band_row)
    
    connection.commit()  # Commit the transaction
    connection.close()

def insert_multiple_bands(multiple_bands_data):
    connection = sqlite3.connect(DB_FILE)
    cursor = connection.cursor()
    
    # Execute SQL query to insert multiple rows
    cursor.executemany(f"INSERT INTO {TABLE} VALUES(?,?,?)", multiple_bands_data)
    
    connection.commit()
    connection.close()




def main():
    # => Fetch band data based on specified criteria
    # data = fetch_band_data(this_band='BAND')
    # data = fetch_band_data(this_date='DATE')
    # print(data)

    # => Insert data for individual bands
    # for band_data in BANDS_DATA:
    #     insert_one_band(band_data)

    # => Insert data for multiple bands
    # insert_multiple_bands(BANDS_DATA)

    # => Fetch all band data
    data = fetch_all_bands_data()
    print(data)


if __name__ == "__main__":
    main()
