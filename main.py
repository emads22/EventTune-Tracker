import requests
import selectorlib
import time
import logging
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
        str: The HTML source code of the webpage.

    """
    # Send a GET request to the URL to retrieve the webpage's HTML content
    # Note: 'headers' parameter is optional, depending on the website's requirements (requests.get(url,headers=HEADERS))
    response = requests.get(url)

    # Extract the HTML source code from the response
    html_source = response.text

    return html_source


def extract(source_text):
    """
    Extract data from the page source using SelectorLib.

    Args:
        source_text (str): The HTML source code of the webpage.

    Returns:
        list: A list containing extracted data based on the defined selectors.
    """
    # Create an extractor object from the YAML configuration file
    e = selectorlib.Extractor.from_yaml_file(YAML_FILE)

    # Extract data from the source text using the defined selectors
    extracted_data = e.extract(source_text)

    # Select the specific key "tours" from the extracted data or [] as default if no data extracted
    extracted_tours = extracted_data.get("tours", [])

    return extracted_tours


def store(data):
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
        if "No upcoming tours" in data:
            return False, "No upcoming tours"

        # Check if the tours file exists
        if not TOURS_FILE.exists():
            # If the file doesn't exist, create it
            with open(TOURS_FILE, 'w'):
                pass  # Create an empty file

        # Check if the tour data is already present in the file
        with open(TOURS_FILE, 'r') as file:
            file_content = file.read()

        if data not in file_content:
            # Append the formatted tour data to the tours file
            with open(TOURS_FILE, 'a') as file:
                file.write(data + '\n')
        else:
            return False, "Tour event already exists"

        # Return success (True) and no error message
        return True, None
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

        # Step 3: Call store function to save the tour data
        success, message = store(extracted_data)

        # Check if the tour data was saved successfully
        if success:
            logging.info("Tour data saved successfully.")

            if send_email(extracted_data):
                logging.info("Email sent successfully.")
            else:
                logging.error("Failed to send email. Please try again later.")
        else:
            logging.error(f"Tour data not saved. Reason: {message}")
    except Exception as e:
        logging.error(f"An error occurred: {e}")


# Entry point of the program
if __name__ == "__main__":
    # Get the start time in seconds since the epoch
    start = time.time()

    # Loop until DURATION in seconds have passed as a trial of running program non-stop
    # we can also use automation on:  https://www.pythonanywhere.com/
    while True:
        # If the current time is more than DURATION in seconds ahead of the starting time, exit the loop
        if time.time() > start + DURATION:
            print(f"\n- Exiting Program: {DURATION} seconds have passed.\n")
            break

        # Call the main function
        main()

        # Pause execution for PAUSE seconds
        time.sleep(PAUSE)
