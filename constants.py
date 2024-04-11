
import os
from pathlib import Path
from dotenv import load_dotenv


# Load environment variables from the .env file
load_dotenv()


ASSETS_DIR = Path("./assets")
YAML_FILE = ASSETS_DIR / "Selectors" / "selectors.yaml"
TOURS_FILE = ASSETS_DIR / "Tours" / "tours.txt"
DATABASE = ASSETS_DIR / "Tours" / "tours.db"
TABLE = "events"
READ_ALL_ROWS_QUERY = f"SELECT * FROM {TABLE}"
INSERT_ROW_QUERY = f"INSERT INTO {TABLE} VALUES(?, ?, ?)"
DURATION = 10
PAUSE = 2

URL = "http://programmer100.pythonanywhere.com/tours/"
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}

SMTP_HOST = "smtp.gmail.com"
SMTP_PORT = 587
SENDER = os.getenv("USER")
PASSWORD = os.getenv("PASSWORD")
RECEIVER = os.getenv("RECEIVER")
