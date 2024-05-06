import os
import smtplib
from email.message import EmailMessage
from pathlib import Path
import logging
from app_logging import handle_logging
from constants import SMTP_HOST, SMTP_PORT, SENDER, PASSWORD, RECEIVER, EMAIL_SUBJECT


# Set up logging using the custom handler
handle_logging()


def send_email(new_event):
    """
    Send an email notification about a new tour event.

    Args:
        new_event (str): A string containing information about the new tour in the format 'Band, City, Date'.

    Returns:
        bool: True if the email was successfully sent, False otherwise.
    """
    # Create an EmailMessage object
    email_message = EmailMessage()

    # Set email subject
    email_message["Subject"] = EMAIL_SUBJECT

    # Split the input data string into band, city, and date
    band, city, date = new_event.split(',')

    # Format the tour data into a readable format
    formatted_data = f'- New tour event on {date.strip()} in {city.strip()}: {
        band.strip()}'

    # Set email content
    email_message.set_content(formatted_data)

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


if __name__ == "__main__":

    test_file_path = Path("./assets") / "Tours" / "tours.txt"

    if send_email(test_file_path):
        print("\n--- Email sent successfully. ---\n")
    else:
        print("\n--- Failed to send email. Please try again later. ---\n")
