# RKI-Scraper
In this repository you find two Python-Scrapers which are scraping information about daily covid cases in Germany from the offical website of the German federal government agency and research institute responsible for disease control and prevention Robert Koch Institute (RKI)
The scripts achive two different objectives and have two different methods to save the data.
- The scraping of the **live daily** reported covid cases from https://www.rki.de/DE/Content/InfAZ/N/Neuartiges_Coronavirus/Fallzahlen.html and saving them into a **mysql database**
- The scraping of **past data** from PDF files of the RKI-Situation-Reports and save the data in **textfiles**
(e.g. https://www.rki.de/DE/Content/InfAZ/N/Neuartiges_Coronavirus/Situationsberichte/Dez_2020/2020-12-08-de.pdf?__blob=publicationFile)

### Scrape Covid daily German covid cases:
Set up your database and provide the login information to the mysql.connector.connect function and run `python3 RKI-HTML-Scraper.py`. You can automate the data retreiving by setting up a daily cron job for this command.

### Scrape Covid Cases past German covid cases:
Define the startDate and endDate variable for the case information you want to retreive and run `python3 RKI-PDF-Scraper.py`.
