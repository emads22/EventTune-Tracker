
import os
from pathlib import Path
from dotenv import load_dotenv


# Load environment variables from the .env file
load_dotenv()


ASSETS_DIR = Path("./assets")
YAML_FILE = ASSETS_DIR / "Selectors" / "selectors.yaml"
EVENTS_FILE = ASSETS_DIR / "Musical Events" / "events.json"
DATABASE_FILE = ASSETS_DIR / "Musical Events" / "events.db"
LOG_FILE = ASSETS_DIR / "Logs" / "app.log"

TABLE = "events"
CREATE_TABLE_QUERY = f"""
CREATE TABLE IF NOT EXISTS {TABLE} (
    artist TEXT,
    location TEXT,
    date TEXT,
    url TEXT
)
"""
# Insert the event data into the table with ignoring duplicates
INSERT_ROW_QUERY = f"""INSERT OR IGNORE INTO {
    TABLE} (artist, location, date, url) VALUES (?, ?, ?, ?)"""

DURATION = 10  # 10 seconds
PAUSE = 2  # 2 seconds

URL = "https://www.bandsintown.com/today/genre/all-genres?recommended_artists_filter=All+Artists#search"
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}

EMAIL_SUBJECT = "Today's Must-See Musical Events! 🎶 Don't Miss Out!"
SMTP_HOST = "smtp.gmail.com"
SMTP_PORT = 587
SENDER = os.getenv("USER")
PASSWORD = os.getenv("PASSWORD")
RECEIVER = os.getenv("RECEIVER")

ASCII_ART = """

███████╗██╗   ██╗███████╗███╗   ██╗████████╗████████╗██╗   ██╗███╗   ██╗███████╗    ████████╗██████╗  █████╗  ██████╗██╗  ██╗███████╗██████╗ 
██╔════╝██║   ██║██╔════╝████╗  ██║╚══██╔══╝╚══██╔══╝██║   ██║████╗  ██║██╔════╝    ╚══██╔══╝██╔══██╗██╔══██╗██╔════╝██║ ██╔╝██╔════╝██╔══██╗
█████╗  ██║   ██║█████╗  ██╔██╗ ██║   ██║█████╗██║   ██║   ██║██╔██╗ ██║█████╗         ██║   ██████╔╝███████║██║     █████╔╝ █████╗  ██████╔╝
██╔══╝  ╚██╗ ██╔╝██╔══╝  ██║╚██╗██║   ██║╚════╝██║   ██║   ██║██║╚██╗██║██╔══╝         ██║   ██╔══██╗██╔══██║██║     ██╔═██╗ ██╔══╝  ██╔══██╗
███████╗ ╚████╔╝ ███████╗██║ ╚████║   ██║      ██║   ╚██████╔╝██║ ╚████║███████╗       ██║   ██║  ██║██║  ██║╚██████╗██║  ██╗███████╗██║  ██║
╚══════╝  ╚═══╝  ╚══════╝╚═╝  ╚═══╝   ╚═╝      ╚═╝    ╚═════╝ ╚═╝  ╚═══╝╚══════╝       ╚═╝   ╚═╝  ╚═╝╚═╝  ╚═╝ ╚═════╝╚═╝  ╚═╝╚══════╝╚═╝  ╚═╝
                                                                                                                              
"""