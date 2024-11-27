import time
import requests as req
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
from concurrent.futures import ThreadPoolExecutor, as_completed
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import csv
import pandas as pd
import os

class Scraper:
    def __init__(self, url, max_workers=5):
        self.url = url
        self.max_workers = max_workers

    @staticmethod
    def getdriver():
        chrome_options = Options()
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument("--disable-setuid-sandbox")
        chrome_options.add_argument("--headless")

        
        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=chrome_options)
        return driver
        
    def getNUI(self, code):
        driver = self.getdriver()
        try:
            driver.get(self.url)
            print("Page loaded")
            
            # Wait for and find the select input field
            select_input = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, 'input.mantine-Input-input.mantine-Select-input[placeholder="Zgjedhe"]'))
            )
            select_input.click()
            print("Clicked dropdown")
            
            # Enter the code
            select_input.send_keys(code)
            print("Entered code")
            
            # Wait for dropdown items to appear and click the first one
            dropdown_item = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, '[class*="mantine-"][class*="-item"]'))
            )
            print("Found dropdown item")
            dropdown_item.click()
            print("Clicked dropdown item")
            
            # Wait for and click the submit button
            submit_button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, 'button.btn-search-slide[type="submit"]'))
            )
            submit_button.click()
            print("Submit clicked")
            
            # Wait for the table to load and be visible
            time.sleep(3)  # Give some time for data to load
            
            # Wait for the Mantine table to load
            table = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, 'table.mantine-Table-root'))
            )
            
            # Find all business number cells and extract their text
            business_numbers = []
            cells = driver.find_elements(By.CSS_SELECTOR, 'td.mantine-1goavx3')  # This class is specific to the NUI column
            for cell in cells:
                business_numbers.append(cell.text)
            print(f"Found {len(business_numbers)} business numbers")
            
            return business_numbers
            
        except Exception as e:
            print(f"Error during scraping: {str(e)}")
            return []
        finally:
            driver.quit()
    
    def scrapeBusiness(self, NUI):
        driver = self.getdriver()
        try:
            driver.get(self.url)
            print("Page loaded")
            
            # Wait for and find the input field using Mantine classes
            input_field = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, 'input.mantine-Input-input.mantine-TextInput-input[placeholder="Numri Unik Identifikues"]'))
            )
            input_field.send_keys(NUI)
            print("NUI entered")
            
            # Wait for and click the submit button
            submit_button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, 'button.btn-search-slide[type="submit"]'))
            )
            submit_button.click()
            print("Submit clicked")
            
            # Wait for the table to load and be visible
            time.sleep(3)  # Give some time for data to load

            # Wait for the Mantine table to load
            table = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, 'table.mantine-Table-root'))
            )

            # Find and click the business name button in the first column of the first row
            business_name_button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, 'table.mantine-Table-root tbody tr:first-child td:first-child button'))
            )
            business_name_button.click()
            print("Clicked business name")

            # Wait for the details table to load
            time.sleep(3)  # Give some time for data to load
            # Wait for the details table to load
            details_table = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, 'div.table-details table'))
            )
            print("Found details table")

            # Get the table HTML for processing
            table_html = details_table.get_attribute('outerHTML')
            soup = BeautifulSoup(table_html, 'lxml')
            business_data = soup.find_all('tr')
            return self.extract_business_data(business_data)

        except Exception as e:
            print(f"Error scraping business {NUI}: {str(e)}")
            return None
        finally:
            driver.quit()

    def extract_business_data(self, business_data):
        name = business_data[0].find('td').getText().strip()  # Emri i biznesit
        nrbiznesi = business_data[3].find('td').getText().strip()  # Numri unik identifikues
        adresa = business_data[9].find('td').getText().strip()  # Adresa
        status = business_data[13].find('td').getText().strip()  # Statusi në ARBK
        phone = business_data[10].find('td').getText().strip()  # Telefoni
        email = business_data[11].find('td').getText().strip()  # E-mail
        return [name, nrbiznesi, status, adresa, phone, email]

    def scrape_batch(self, nui_list):
        results = []
        with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            # Submit all scraping tasks
            future_to_nui = {executor.submit(self.scrapeBusiness, nui): nui for nui in nui_list}
            
            # Process completed tasks as they finish
            for future in as_completed(future_to_nui):
                nui = future_to_nui[future]
                try:
                    data = future.result()
                    if data:
                        results.append(data)
                except Exception as e:
                    print(f"Error processing NUI {nui}: {str(e)}")
        
        return results
