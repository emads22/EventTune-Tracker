import requests
import selectorlib
import json
import logging
import sqlite3
from app_logging import handle_logging
from send_email import send_email
from constants import *


# Set up logging using the custom handler
handle_logging()


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

        # Select the specific key "events" from the extracted data or [] as default if no data extracted
        # extracted_events = extracted_data.get("events", [])
        return extracted_data
    except Exception as e:
        print(f"Error extracting data: {e}")
        return []


def store_in_file(data):
    """
    Save event data to the events file.

    Args:
        data (dict): A dictionary containing extracted events data with the format:
                     {'events': [
                            {'artist': '...', 
                            'location': '...', 
                            'date': '...', 
                            'url': '...'}, 
                            ...
                            ]}

    Returns:
        tuple: A tuple containing a boolean indicating success or failure (True for success, False for failure) 
               and an error message (if any).
    """
    
    try:
        
        # Check if the 'events' key exists in the input data
        if 'events' not in data or not data['events']:
            return False, "No upcoming events"

        # Ensure parent directories exist; if not, create them
        EVENTS_FILE.parent.mkdir(parents=True, exist_ok=True)

        # if events file does not exist, create the file with initial content
        if not EVENTS_FILE.exists():
            initial_content = {
                'events': []
            }
            with open(EVENTS_FILE, 'w') as json_file:
                json.dump(initial_content, json_file, indent=4)

        # Open the JSON file and read its content
        with open(EVENTS_FILE, 'r') as json_file:
            existing_data = json.load(json_file)

        # Compare and add only the new events to the existing data
        for event in data['events']:
            if event not in existing_data['events']:
                existing_data['events'].append(event)

        # Save the updated content back to the JSON file
        with open(EVENTS_FILE, 'w') as json_file:
            json.dump(existing_data, json_file, indent=4)

        # Return success (True) and no error message
        return True, None
    except Exception as e:
        # Return failure (False) and the error message
        return False, str(e)


def store_in_db(data):
    """
    Store event data in a SQLite database.

    Args:
        data (dict): A dictionary containing extracted events data with the format:
                     {'events': [
                            {'artist': '...', 
                            'location': '...', 
                            'date': '...', 
                            'url': '...'}, 
                            ...
                            ]}

    Returns:
        tuple: A tuple indicating success or failure of the operation along with an optional error message.
               The tuple has the format (success(bool), error_message(str)).
    """
    try:
        # Check if the 'events' key exists in the input data
        if 'events' not in data or not data['events']:
            return False, "No upcoming events"
        
        # Create the database file and connect to it
        if not DATABASE_FILE.exists():
            # If the database file doesn't exist, create it and establish a connection
            with sqlite3.connect(DATABASE_FILE) as connection:
                cursor = connection.cursor()
                # Create the events table
                cursor.execute(CREATE_TABLE_QUERY)

        # Establish the SQLite database connection, using with statement will close connection after finishing
        with sqlite3.connect(DATABASE_FILE) as connection:
            cursor = connection.cursor()

            # Insert the event data into the table, ignoring duplicates, used get() in case theres no value to insert None by default
            for event in data['events']:
                cursor.execute(INSERT_ROW_QUERY, (event.get('artist'), event.get(
                    'location'), event.get('date'), event.get('url')))

            # Commit the transaction
            connection.commit()

        # Return success (True) and no error message
        return True, None

    except sqlite3.Error as e:
        # Handle SQLite errors
        return False, f"SQLite Error: {str(e)}"

    except Exception as e:
        # Handle other exceptions
        return False, str(e)


def main():
    """
    Main function to orchestrate the scraping, extraction, and saving of event data.

    This function initiates the scraping process, extracts event data, and stores it in a file or SQL database.
    """
    try:
        # Step 1: Scrape data from the specified URL
        scraped_data = scrape(URL)

        # Step 2: Extract event data from the scraped content
        extracted_data = extract(scraped_data)

        # # Step 3: Call store function to save the event data in a file
        # success, message = store_in_file(extracted_data)

        # Step 3: Call store function to save the event data in a database
        success, message = store_in_db(extracted_data)

        # Check if the event data was saved successfully
        if success:
            logging.info("Event data saved successfully.")

            if send_email(extracted_data['events']):
                logging.info("Email sent successfully.")
            else:
                logging.error("Failed to send email. Please try again later.")
        else:
            logging.error(f"Event data not saved. Reason: {message}")
    except Exception as e:
        logging.error(f"An error occurred: {e}")


# Entry point of the program
if __name__ == "__main__":

    # Call the main function
    main()

    # Printing a message indicating the program is exiting and displaying the duration.
    print(f"\n--- The email containing today's musical event details has been successfully dispatched. ---\n")

