# OLX Car Cover Scraper

A Python script to scrape car cover listings from OLX India using two methods:

1. **HTML scraping via `requests` and BeautifulSoup** (limited results)
2. **Direct API fetching via OLX's internal API** (more results)

---

## Features

- Scrape product titles, prices, locations, and links via webpage parsing.
- Fetch detailed ad data including username, description, geo-coordinates, and direct OLX links from the API.
- Save scraped data into CSV files for easy analysis.
- User choice to select scraping method.
- Handles pagination for multiple pages.

---

## Requirements

- Python 3.6+
- `requests`
- `beautifulsoup4`

Install dependencies via pip:

```bash
pip install requests beautifulsoup4
```
##Usage
Run the script:

```bash
python olx_scraper.py
```
You'll be prompted to choose the scraping method:

-Enter 1 to scrape via HTML requests (may return fewer results).

-Enter 2 to fetch data from OLX API (more comprehensive results).

For API fetching, you'll also be prompted to enter how many pages to scrape.

##Output
```Python
For method 1 (HTML scraping), data is saved to olx_data_via_requests.csv.

For method 2 (API fetching), data is saved to olx_data_via_curl.csv.
```

Each CSV includes relevant fields such as:
```csv
| Title | Username | Price | Description | Location | Latitude | Longitude | Google Maps Link | OLX Direct Link |
```
##Notes
API scraping uses direct HTTP GET requests with headers for best compatibility.

Be mindful of request rates to avoid getting blocked by OLX.

##This tool is for educational and personal use. Respect OLX's terms of service.

##License
This project is released under the MIT License.

##Contact
For questions or suggestions, please open an issue or contact me at [nnakulvverma8@gmail.com].

Happy scraping! 🚗🛡️