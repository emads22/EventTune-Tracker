import requests
import selectorlib
from datetime import datetime
from pathlib import Path


URL = "http://programmer100.pythonanywhere.com/"
YAML_FILE = Path('./selectors.yaml')
DATA_FILE = Path('./data.txt')


def scrape(url):
    response = requests.get(url)
    html_source = response.text
    return html_source


def extract(source):
    e = selectorlib.Extractor.from_yaml_file(YAML_FILE)
    data = e.extract(source)
    return data["temperatures"]


def store(temperature):

    if not DATA_FILE.exists():
        with open(DATA_FILE, 'w') as file:
            pass

    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    formatted_data = f'{now},{temperature}'

    with open(DATA_FILE, 'a') as file:
        file.write(formatted_data + '\n')


def main():
    page_scraped = scrape(URL)
    temp_extracted = extract(page_scraped)
    store(temp_extracted)


if __name__ == "__main__":
    while True:
        main()
        import time
        time.sleep(3)
