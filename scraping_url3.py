import requests
from bs4 import BeautifulSoup
import psycopg2 # PostgreSQL connector
import logging  # For event logs

# The target URL
URL3 = "https://www.scrapethissite.com/pages/advanced/"

logger = logging.getLogger(__name__)
logging.basicConfig(filename ="logs_url3.log", encoding ='utf-8', level =logging.DEBUG, force = True)

# Function to store data to the PostgreSQL database
def database(data):
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
        cursor.execute("""CREATE TABLE IF NOT EXISTS spoof (
                        ID SERIAL PRIMARY KEY,
                        Text VARCHAR(255)
                        );
                    """)
                
        connect.commit()    # Add all changes
                
        query="INSERT INTO spoof (Text) VALUES ('{0}');".format(str(data))
        cursor.execute(query)
        connect.commit()    # Add all changes
        print("Done")

    except:
        logging.exception("An error occurred while storing data to the database. Check the logs:\n")
        print("Error encountered while storing data to the database. Check the log file.")

    finally:
        connect.close() # Close the database connection

def spoof_headers(url):
    headers = {'Accept': 'text/html', 'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'} #specifying the spoofed headers
    url += "?gotcha=headers"
    response = requests.get(url, headers=headers)
    response.close()    # Close the session
    soup = BeautifulSoup(response.text, "html.parser")
    text=soup.find("div", class_= "col-md-4 col-md-offset-4")
    return text.text.strip()

try:
    spoof_data = spoof_headers(URL3)    # Function call
    print("Scraping and sanitizing done...storing data in a PostgreSQL database")
except:
    logging.exception("An error occurred. Check the logs:\n")
    print("Error encountered. Check the log file.")

database(spoof_data)    # Function call