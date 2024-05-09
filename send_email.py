import os
import smtplib
from email.message import EmailMessage
from pathlib import Path
import logging
from app_logging import handle_logging
from constants import SMTP_HOST, SMTP_PORT, SENDER, PASSWORD, RECEIVER, EMAIL_SUBJECT


# Set up logging using the custom handler
handle_logging()


def send_email(events):
    """
    Send an email notification about new events.

    Args:
        events (list): A list of dictionaries where each dictionary represents event data. Each event dictionary 
                       should contain the following keys: 'artist' (str), 'location' (str), 'date' (str), and 
                       'url' (str), representing the artist's name, event location, date of the event, and URL 
                       for more information, respectively.

    Returns:
        bool: True if the email was successfully sent, False otherwise.
    """
    # Create an EmailMessage object
    email_message = EmailMessage()

    # Set email subject
    email_message["Subject"] = EMAIL_SUBJECT

    # Initialize email content
    email_content = f"- Musical events on today {events[0].get('date').split('-')[0].strip()}:\n\n"

    # Iterate through the events
    for i, event in enumerate(events):
        # Format the event data into a readable format
        email_content += f"""
- Event {i+1}:
    . Artist:  {event.get('artist')}
    . Location:  {event.get('location')}
    . Start Time:  {event.get('date')}
    . More info:  {event.get('url')}

"""
    # Set email content
    email_message.set_content(email_content)

    try:
        # Connect to the SMTP server
        with smtplib.SMTP(SMTP_HOST, SMTP_PORT) as smtp_server:
            smtp_server.ehlo()  # Introduce ourselves to the server
            smtp_server.starttls()  # Upgrade the connection to a secure one using TLS
            smtp_server.login(SENDER, PASSWORD)  # Login to the SMTP server
            # Send the email via SMTP after converting the message to a string
            smtp_server.sendmail(SENDER, RECEIVER, email_message.as_string())

        # Return True if the email was successfully sent
        return True

    except smtplib.SMTPException as e:
        # Log the error if an SMTPException occurs
        logging.exception(f"Failed to send email: {e}")

        # Return False indicating failure to send email
        return False



