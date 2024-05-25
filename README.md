# VakilDesk Interview Assignment: Web Scraping Project

This repository contains the code for a web scraping project completed as an interview assignment for VakilDesk.

# Project Overview:

This project scrapes data from three different URLs and stores it in a PostgreSQL database. However, since the 'Logins & Session Data' and 'CSRF & Hidden Values' parts of URL 3 apparently require logging into the website, and the Sign Up page appears to be behind a paywall, I was not able to scrape them. For URL 3, the code only works for the 'Spoofing Headers' part.

# Target URLs:

URL 1: https://www.scrapethissite.com/pages/ajax-javascript/#2015

URL 2: https://www.scrapethissite.com/pages/forms/

URL 3: https://www.scrapethissite.com/pages/advanced/  (Login required, functionality not fully implemented)

# Scraped Data:

Data extracted from each URL will be stored in separate tables within the 'postgres' database of PostgreSQL.

films (for URL 1)

hockey (for URL 2)

spoof (for URL 3 'Spoofing Headers' part)

# Logging:

Script execution logs detailed information for each URL in separate log files.

logs_url1.log (for URL 1)

logs_url2.log (for URL 2)

logs_url3.log (for URL 3)

# Technical Specifications:

Programming Language: Python 3.11.6

Libraries:

BeautifulSoup 4.12.2

Requests 2.31.0

Pyppeteer 1.0.0 (Note: downgraded after installing Requests-HTML)

Psycopg2 2.9.9 (dt dec pq3 ext lo64)

Logging 0.5.1.2

Requests-HTML

Database: PostgreSQL (tables created on execution)

Operating System: Windows 11 x64

# Project Limitations:

URL 3 partially scraped due to Login requirements.

# Running the Script

Ensure you have Python 3.11.6 and the required libraries installed.

Navigate to the project directory in your terminal/cmd.

Execute the script using: 'python main.py' or 'python3 main.py'

Once data is scraped, the script will ask for PostgreSQL username, host, password and port on which the server is listening.

The tables will be created in the 'postgres' database.

# Log Files

Log files for each URL will be created in the same directory.

# Encoding

Log files are encoded in UTF-8. If encountering encoding issues, try changing it to Latin-1.
