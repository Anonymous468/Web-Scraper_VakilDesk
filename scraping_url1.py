from bs4 import BeautifulSoup
from requests_html import HTMLSession   # This extension of requests library helps to scrap dynamically loaded webpages
import psycopg2 # PostgreSQL connector
import logging  # For event logs
import sys

# The target URL
URL1 = "https://www.scrapethissite.com/pages/ajax-javascript/#2015"

logger = logging.getLogger(__name__)
logging.basicConfig(filename ="logs_url1.log", encoding ='utf-8', level =logging.DEBUG, force = True)

# Function to store data to the PostgreSQL database
def database(film_titles,film_nominations,film_awards,film_best_picture):
    try:
        # Using the default database, 'postgres'
        user = input("Enter username: ")
        password = input("Enter password: ")
        host = input("Enter host (localhost or remote): ")
        port = input("Enter port number on which the server is listening: ")

        # Connection establishment
        connect = psycopg2.connect(
                database = "postgres",
                user = user,
                password = password,
                host = host,
                port = port
                )
                  
        # Creating a cursor object
        cursor = connect.cursor()
                
        # Create films table if it does not exist
        cursor.execute("""CREATE TABLE IF NOT EXISTS films (
                        ID SERIAL PRIMARY KEY,
                        Title VARCHAR(255),
                        Nominations INT,
                        Awards INT,
                        Best_Picture VARCHAR(10)
                        );
                    """)
                
        connect.commit()    # Add all changes
                
        for i in range(len(film_titles)):
            query="INSERT INTO films (Title, Nominations, Awards, Best_Picture) VALUES (%s,%s,%s,%s);"
            param=(film_titles[i],film_nominations[i],film_awards[i],film_best_picture[i])
            cursor.execute(query,param) # SQL Injection prevention
            connect.commit()    # Add all changes
        print("Done")

    except:
        logging.exception("An error occurred while storing data to the database. Check the logs:\n")
        print("Error encountered while storing data to the database. Check the log file.")

    finally:
        connect.close() # Close the connection


# Function to scrape data from URL1
def scraping_url1(url):
    try:
        session = HTMLSession()
        response = session.get(url)    # Sending GET request
        
        if response.status_code >= 200 and response.status_code < 300:  # Execute only if the status code is 2XX
            response.html.render(sleep=10)  # Waiting for JavaScript to render
            soup = BeautifulSoup(response.html.html, 'html.parser')  # Parsing the fetched contents
            
            # The required data in list form but with HTML tags
            film_titles = soup.find_all("td", class_="film-title")
            film_nominations = soup.find_all("td", class_="film-nominations")
            film_awards = soup.find_all("td", class_="film-awards")
            film_best_picture = soup.find_all("td", class_="film-best-picture")
            
            session.close()

            for i in range(len(film_titles)):   # This loop will remove the HTML tags from each data
                film_titles[i] = (film_titles[i].text).strip()
                film_nominations[i] = (film_nominations[i].text).strip()
                film_awards[i] = (film_awards[i].text).strip()
                if film_titles[i] == "Spotlight":
                    film_best_picture[i] = "Flag"
                else:
                    film_best_picture[i] = "NULL"

            print("Scraping and sanitizing done...storing data in a PostgreSQL database")

            database(film_titles,film_nominations,film_awards,film_best_picture)            # Function call

        else:
            logging.exception(f"Status code {response.status_code} received\n")
            sys.exit("Terminating...Check the log file")
            
    except:
        logging.exception("An error occurred. Check the logs:\n")
        print("Error encountered. Check the log file")

    finally:
        try:
            session.close()
        except:
            pass


scraping_url1(URL1) # Function call