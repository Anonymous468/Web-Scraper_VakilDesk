from bs4 import BeautifulSoup
from requests_html import HTMLSession   # This extension of requests library helps to scrap dynamically loaded webpages
import psycopg2 # PostgreSQL connector
import logging  # For event logs

# The target URL
URL2 = "https://www.scrapethissite.com/pages/forms/"

logger = logging.getLogger(__name__)
logging.basicConfig(filename ="logs_url2.log", encoding ='utf-8', level =logging.DEBUG, force = True)

#Initializing the parent lists to store data from each page
all_teams = []
all_years = []
all_wins = []	
all_losses = []
all_ot = []
all_win_percent = []
all_gf = []	
all_ga = []
all_diff = []


# Function to store data to the PostgreSQL database
def database(all_teams, all_years, all_wins, all_losses, all_ot, all_win_percent, all_gf, all_ga, all_diff):
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
        cursor.execute("""CREATE TABLE IF NOT EXISTS hockey (
                        ID SERIAL PRIMARY KEY,
                        Team_Name VARCHAR(255),
                        Year INT,
                        Wins INT,
                        Losses INT,
                        OT_Losses VARCHAR(10),
                        Win_percent FLOAT,
                        Goals_For INT,
                        Goals_Against INT,
                        Diff INT
                        );
                    """)
                
        connect.commit()    # Add all changes
                
        for i in range(len(all_teams)):
            query="INSERT INTO hockey (Team_Name, Year, Wins, Losses, OT_Losses, Win_percent, Goals_For, Goals_Against, Diff) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s);"
            param=(all_teams[i], all_years[i], all_wins[i], all_losses[i], all_ot[i], all_win_percent[i], all_gf[i], all_ga[i], all_diff[i])
            cursor.execute(query,param) # SQL Injection prevention
            connect.commit()    # Add all changes
        print("Done")

    except:
        logging.exception("An error occurred while storing data to the database. Check the logs:\n")
        print("Error encountered while storing data to the database. Check the log file.")

    finally:
        connect.close() # Close the connection


# Function to scrape data from URL2
def scraping_url2(url,j):
    
    global all_teams, all_years, all_wins, all_losses, all_ot, all_win_percent, all_gf, all_ga, all_diff    #declaring them as global variables
    try:
        
        url+=f"?page_num={j}"   # adding the page number part to the URL
        
        session = HTMLSession()
        response = session.get(url)    # Sending GET request
        
        if response.status_code >= 200 and response.status_code < 300:  # Execute only if the status code is 2XX
            response.html.render(sleep=10)  # Waiting for JavaScript to render
            soup = BeautifulSoup(response.html.html, 'html.parser')  # Parsing the fetched contents

            # Find all <tr> tags in the page
            tr_tags = soup.find_all("tr", class_="team")
            # Add data to the parent list after sanitizing it
            for i in tr_tags:
                #soup1=BeautifulSoup(i, 'html.parser')
                all_teams.append((i.find("td", class_="name").text).strip())
                all_years.append((i.find("td", class_="year").text).strip())
                all_wins.append((i.find("td", class_="wins").text).strip())
                all_losses.append((i.find("td", class_="losses").text).strip())
                all_ot.append((i.find("td", class_="ot-losses").text).strip())
                all_gf.append((i.find("td", class_="gf").text).strip())
                all_ga.append((i.find("td", class_="ga").text).strip())
                pct_success = i.find("td", class_="pct text-success")
                pct_danger = i.find("td", class_="pct text-danger")
                diff_success = i.find("td", class_="diff text-success")
                diff_danger = i.find("td", class_="diff text-danger")
                
                # Handling multiple classes in Win % and +/- columns
                if pct_success!=None:
                    all_win_percent.append((pct_success.text).strip())
                else:
                    all_win_percent.append((pct_danger.text).strip())

                if diff_success!=None:
                    all_diff.append((diff_success.text).strip())
                else:
                    all_diff.append((diff_danger.text).strip())                
            
            session.close()
                
            print(f"Page {j} done")

        else:
            logging.exception(f"Status code {response.status_code} received for page {j}\n")
            
    except:
        logging.exception("An error occurred. Check the logs:\n")
        print("Error encountered. Check the log file")

    finally:
        try:
            session.close()
        except:
            pass


for j in range(1,25):   # Iteratively access each page
    scraping_url2(URL2,j) # Function call

# Sanitizing the scrapped data
try:
    for i in range(len(all_ot)):    #Handling empty strings in OT column
        if all_ot[i] == "":
            all_ot[i] = "NULL"

    print("Scraping and sanitizing done...storing data in a PostgreSQL database")

except:
    logging.exception("An error occurred while sanitizing the data. Check the logs:\n")
    print("Error encountered while sanitizing the data. Check the log file")

database(all_teams, all_years, all_wins, all_losses, all_ot, all_win_percent, all_gf, all_ga, all_diff)            # Function call
