import sys

print("1) Scrape first URL\n2) Scrape second URL\n3) Scrape third URL\n4) Clear the three log files\n")
choice=input("Enter your choice (1, 2, 3 or 4): ")
print("\n")
if choice == '1':
    with open("scraping_url1.py") as f:
        exec(f.read())
elif choice == '2':
    with open("scraping_url2.py") as f:
        exec(f.read())
elif choice == '3':
    with open("scraping_url3.py") as f:
        exec(f.read())
elif choice == '4':
    with open('logs_url1.log', 'w'):
        pass
    with open('logs_url2.log', 'w'):
        pass
    with open('logs_url3.log', 'w'):
        pass
else:
    sys.exit("Wrong choice entered. Terminating...")