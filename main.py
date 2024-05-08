import requests
import selectorlib
import time
from datetime import datetime, timedelta
import json
import logging
import sqlite3
from app_logging import handle_logging
from send_email import send_email
from constants import *
import t


# Set up logging using the custom handler
handle_logging()

# Establish the database connection
connection = sqlite3.connect(DATABASE)


def scrape(url):
    """
    Scrape the HTML source code from the given URL.

    Args:
        url (str): The URL of the webpage to scrape.

    Returns:
        str: The HTML source code of the webpage, or None if an error occurs.
    """
    try:
        # Send a GET request to the URL to retrieve the webpage's HTML content
        response = requests.get(url, headers=HEADERS)
        response.raise_for_status()  # Raise an exception for 4xx or 5xx status codes

        # Extract the HTML source code from the response
        html_source = response.text
        return html_source
    except requests.RequestException as e:
        print(f"Error fetching URL: {e}")
        return None


def extract(source_text):
    """
    Extract data from the page source using SelectorLib.

    Args:
        source_text (str): The HTML source code of the webpage.

    Returns:
        list: A list containing extracted data based on the defined selectors.
    """
    try:
        # Create an extractor object from the YAML configuration file
        e = selectorlib.Extractor.from_yaml_file(YAML_FILE)

        # Extract data from the source text using the defined selectors
        extracted_data = e.extract(source_text)

        # Select the specific key "tours" from the extracted data or [] as default if no data extracted
        extracted_tours = extracted_data.get("tours", [])
        return extracted_tours
    except Exception as e:
        print(f"Error extracting data: {e}")
        return []


def store_in_file(data):
    """
    Save tour data to the tours file.

    Args:
        data (str): The tour data string in the format 'Tour Name, Location, Date'.

    Returns:
        tuple: A tuple containing a boolean indicating success or failure (True for success, False for failure) 
               and an error message (if any).
    """
 
    try:
        # Check if the input data indicates no upcoming tours
        if len(data) == 0:
            return False, "No upcoming tours"

        # Ensure parent directories exist, if not, create them
        TOURS_FILE.parent.mkdir(parents=True, exist_ok=True)

        # Create the file with specific content
        if not TOURS_FILE.exists():
            with open(TOURS_FILE, 'w') as json_file:
                json_file.write('{"tours":[]}')  # {} means empty dict
        
        # Step 1: Open the JSON file and read its content
        with open(TOURS_FILE, 'r') as json_file:
            existing_data = json.load(json_file)

        
        
        # Compare and add only the new tours to the existing data
        for new_tour in data:
            if new_tour not in existing_data['tours']:
                existing_data['tours'].append(new_tour)

        
        # Save the updated content back to the JSON file
        with open(TOURS_FILE, 'w') as json_file:
            json.dump(existing_data, json_file, indent=4)

        # Return success (True) and no error message
        return True, None
    except Exception as e:
        # Return failure (False) and the error message
        return False, str(e)


def store_in_db(data):
    """
    Store tour event data in the database.

    Args:
        data (str): A string containing information about the tour event in the format 'band, city, date'.

    Returns:
        tuple: A tuple indicating success or failure of the operation along with an optional error message.
               The tuple has the format (success(bool), error_message(str)).
    """
    try:
        # Check if the input data indicates no upcoming tours
        if "No upcoming tours" in data:
            return False, "No upcoming tours"

        # Get cursor object to execute SQL queries
        cursor = connection.cursor()

        # Retrieve all rows from the database
        cursor.execute(READ_ALL_ROWS_QUERY)
        all_rows = cursor.fetchall()

        # Split the input data string into band, city, and date, and create a tuple (band, city, date) as a row
        row = tuple(item.strip() for item in data.split(','))

        # Check if this row is already present in the database
        if row not in all_rows:
            cursor.execute(INSERT_ROW_QUERY, row)
            connection.commit()
        else:
            return False, "Tour event already exists"

        # Return success (True) and no error message
        return True, None

    except sqlite3.Error as e:
        # Handle SQLite errors separately
        connection.rollback()  # Rollback the transaction
        return False, f"SQLite Error: {str(e)}"

    except Exception as e:
        # Return failure (False) and the error message
        return False, str(e)


def main():
    """
    Main function to orchestrate the scraping, extraction, and saving of tour data.

    This function initiates the scraping process, extracts tour data, and stores it in a file or SQL database.
    """
    try:
        # Step 1: Scrape data from the specified URL
        scraped_data = scrape(URL)

        # Step 2: Extract tour data from the scraped content
        extracted_data = extract(scraped_data)

        # # Step 3: Call store function to save the tour data in a file
        success, message = store_in_file(extracted_data)

        # Step 3: Call store function to save the tour data in a database
        # success, message = store_in_db(extracted_data)

        # Check if the tour data was saved successfully
        if success:
            logging.info("Tour data saved successfully.")

            # if send_email(extracted_data):
            #     logging.info("Email sent successfully.")
            # else:
            #     logging.error("Failed to send email. Please try again later.")
        else:
            logging.error(f"Tour data not saved. Reason: {message}")
    except Exception as e:
        logging.error(f"An error occurred: {e}")


# Entry point of the program
if __name__ == "__main__":
    # Get the current time as start_time
    start_time = datetime.now()

    # Calculate end_time by adding the desired duration to start_time
    duration = timedelta(seconds=DURATION)
    end_time = start_time + duration

    # Loop until DURATION in seconds have passed as a trial of running program non-stop
    # we can also use automation on:  https://www.pythonanywhere.com/
    while datetime.now() < end_time:

        # Call the main function
        main()

        # Pause execution for PAUSE seconds
        time.sleep(PAUSE)

    print(f"\n- Exiting Program: {DURATION} seconds have passed.\n")

    # # Finally close the database connection
    # connection.close()
    # main()