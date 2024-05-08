
import os
from pathlib import Path
from dotenv import load_dotenv


# Load environment variables from the .env file
load_dotenv()


ASSETS_DIR = Path("./assets")
YAML_FILE = ASSETS_DIR / "Selectors" / "selectors.yaml"
# YAML_FILE = "./new.yaml"
# TOURS_FILE = ASSETS_DIR / "Tours" / "tours.txt"
TOURS_FILE = ASSETS_DIR / "Tours" / "tours_data.json"
DATABASE = ASSETS_DIR / "Tours" / "tours.db"
TABLE = "events"
READ_ALL_ROWS_QUERY = f"SELECT * FROM {TABLE}"
INSERT_ROW_QUERY = f"INSERT INTO {TABLE} VALUES(?, ?, ?)"
DURATION = 10
PAUSE = 2

# URL = "http://programmer100.pythonanywhere.com/tours/"
# URL = "https://books.toscrape.com/catalogue/category/books/romance_8/index.html"
URL = "https://www.bandsintown.com/today/genre/all-genres?recommended_artists_filter=All+Artists#search"
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}

SMTP_HOST = "smtp.gmail.com"
SMTP_PORT = 587
SENDER = os.getenv("USER")
PASSWORD = os.getenv("PASSWORD")
RECEIVER = os.getenv("RECEIVER")
EMAIL_SUBJECT = "New Tour Event coming up!"
# EMAIL_SUBJECT = "Today's Must-See Musical Events in Venice! 🎶 Don't Miss Out!"



# Ensure parent directories exist, if not, create them
# file_path.parent.mkdir(parents=True, exist_ok=True)

# # Create the file
# file_path.touch()