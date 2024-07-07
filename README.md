# EventTune Tracker

![EventTune_Tracker_logo](./assets/Images/EventTune_Tracker_logo.png)

## Overview
EventTune Tracker is a Python application designed to scrape HTML source code from a specific website, extract music event data, and store it for further use. It utilizes the `requests` library for web scraping, `SelectorLib` for data extraction, and supports storing data in either files or SQLite databases. The application also includes features for error handling, logging, and email notification upon successful data processing.

The default website for scraping is [Bandsintown's Today page](https://www.bandsintown.com/today/genre/all-genres?recommended_artists_filter=All+Artists#search), which provides information about music events happening today across various genres. Users can customize the scraping behavior by modifying the SelectorLib YAML file and configure storage options in the `constants.py` file.

## Features
- **Scraping**: Utilizes the `requests` library to scrape HTML source code from a URL.
- **Extraction**: Uses SelectorLib for data extraction based on defined selectors.
- **Storage**: Saves music event data either in a file or an SQLite database, checking for duplicates.
- **Error Handling**: Catches general exceptions and SQLite errors separately, providing informative error messages.
- **Logging**: Logs events to facilitate debugging and monitoring.
- **Email Notification**: Sends email notifications upon successful data processing.
- **Modular Design**: Separates concerns into different functions for improved readability and maintainability.
- **Documentation**: Includes clear docstrings for functions to explain their purpose and parameters.

## Technologies Used
- **python-dotenv**: For managing environment variables.
- **requests**: For making HTTP requests to fetch web page data.
- **selectorlib**: For extracting specific data from web pages.
- **smtplib**: For sending email notifications.
- **logging**: For tracking events that happen when the software runs.

## Setup
1. Clone the repository.
2. Ensure Python 3.x is installed.
3. Install the required dependencies using `pip install -r requirements.txt`.
4. Configure the necessary parameters such as URL, file paths, database details, etc., in `constants.py`.
   - If using the SQLite database option, ensure that you have SQLite installed.
   - Create the required `.db` files (e.g., `events.db`) using DB Browser for SQLite or any other SQLite client. Alternatively, you can create the databases programmatically by running Python scripts to create tables as needed.
5. The default URL for scraping is [Bandsintown's Today page](https://www.bandsintown.com/today/genre/all-genres?recommended_artists_filter=All+Artists#search). You can change it in the `constants.py` file if needed.
6. Run the script using `python main.py`.

## Usage
1. Run the script using `python main.py`.
2. Monitor the logs for any errors or notifications.
3. Check the specified file or database for stored music event data.
4. Optionally, configure email settings for notifications.

## Contributing
Contributions are welcome! Here are some ways you can contribute to the project:
- Report bugs and issues
- Suggest new features or improvements
- Submit pull requests with bug fixes or enhancements

## Author
- Emad
  [<img src="https://img.shields.io/badge/GitHub-Profile-blue?logo=github" width="150">](https://github.com/emads22)

## License
This project is licensed under the MIT License, which grants permission for free use, modification, distribution, and sublicense of the code, provided that the copyright notice (attributed to [emads22](https://github.com/emads22)) and permission notice are included in all copies or substantial portions of the software. This license is permissive and allows users to utilize the code for both commercial and non-commercial purposes.

Please see the [LICENSE](LICENSE) file for more details.
