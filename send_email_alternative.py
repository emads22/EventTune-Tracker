import smtplib
import ssl
from constants import SMTP_HOST, SMTP_PORT, SENDER, PASSWORD, RECEIVER, EMAIL_SUBJECT


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
    # Initialize email content
    email_content = f"""Subject: {EMAIL_SUBJECT}

- Musical events on today {events[0].get('date').split('-')[0].strip()}:\n\n
"""

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
        
    # Create a SSL context for secure connection
    context = ssl.create_default_context()

    # Connect to the SMTP server using SMTP_SSL
    with smtplib.SMTP_SSL(SMTP_HOST, SMTP_PORT, context=context) as server:
        # Login to the SMTP server
        server.login(SENDER, PASSWORD)

        # Send the email message
        server.sendmail(SENDER, RECEIVER, email_content)
