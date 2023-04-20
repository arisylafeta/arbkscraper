

      Welcome to ARBK SCRAPER
=====================================

This program will help you scrape both ARBK Business NUI's and ARBK Business data.
The program requires as input activity code, or a text file with NUI's, and can be run in any machine that has Python installed. 

            REQUIREMENTS!
====================================
Selenium WebDriver : https://pypi.org/project/selenium/ : pip install selenium
Webdriver Manager : https://pypi.org/project/webdriver-manager/ : pip install webdriver-manager
Beautiful Soup : https://pypi.org/project/beautifulsoup4/ : pip install bs4
LXML : https://pypi.org/project/lxml/ : pip install lxml

Chrome Webdriver : https://chromedriver.chromium.org/downloads !!IMPORTANT!! CHECK helper.py, and modify PATH variable inline with the directory you've extracted chromedriver.exe to.



          USER ADJUSTMENTS
=====================================
Program parses the following info for businesses: name, NUI, address, status, phone, email. In order to edit the data parsed check main.py > scrapeBusiness function.

Check main.py for instructions on how to utilize multiple threads while scraping ARBK data
