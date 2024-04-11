import smtplib
import ssl
from constants import SMTP_HOST, SMTP_PORT, SENDER, PASSWORD, RECEIVER


def send_email(new_event):
    """
    Send an email about a new tour event using SMTP_SSL protocol.

    Args:
        new_event (str): A string containing information about the new tour event.
                        The string should be in the format 'band, city, date'.

    Raises:
        smtplib.SMTPException: If an error occurs during the SMTP communication.

    Returns:
        None
    """
    # Split the input data string into tour name, city, and date
    band, city, date = new_event.split(',')

    # Format the tour data into a readable format with subject
    subject = f'New Tour Event coming up!'
    formatted_message = f"""Subject: {subject}

- New tour event on {date.strip()} in {city.strip()}: {band.strip()}"""

    # Create a SSL context for secure connection
    context = ssl.create_default_context()

    # Connect to the SMTP server using SMTP_SSL
    with smtplib.SMTP_SSL(SMTP_HOST, SMTP_PORT, context=context) as server:
        # Login to the SMTP server
        server.login(SENDER, PASSWORD)

        # Send the email message
        server.sendmail(SENDER, RECEIVER, formatted_message)
