# Znany Lekarz Scraper

## Overview

The ZnanyLekarz Scraper is a Python program designed to scrape data from 
the www.znanylekarz.pl website, specifically targeting information about 
different medical specialists in Poland. The scraped data is stored in an 
SQLite database for better organization and management.

## How It Works

The program follows a straight forward workflow:

1. The user is prompted to select the index of the medical specialization type.
2. The user specifies the number of pages to traverse for scraping data.
3. The program scrapes the relevant information from the selected pages on the website.
4. The scraped data is stored in an SQLite database.
5. To verify the correctness of the saved data, you can utilize the dboperations script. Modify the script as needed to suit your specific requirements.


## Getting Started

### Prerequisities

* Python 3.x

### Installation

1. Clone the repository:
```
git clone https://github.com/Janasu97/znanylekarz-scraper.git
```
2. Navigate to the project directory:
3. Install the required Python packages:

```
pip3 install requests
pip3 install BeautifulSoup4
pip3 install matplotlib
```

## Usage

1. Run the main scraper script:
```
python main.py
```

Follow the on-screen prompts to select the specialization type 
index and specify the number of pages to scrape.
 
2. To check and manipulate the stored data, use the dboperations script:

```
python dboperations.py
```

Modify the script according to your needs for database operations.

## Contributing

Contributions are welcome! If you find any issues or have 
suggestions for improvements, feel free to open an issue or submit a pull request.

## Authors

Jakub J.
