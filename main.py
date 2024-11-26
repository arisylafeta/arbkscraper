import time
import requests as req
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
from concurrent.futures import ThreadPoolExecutor, as_completed
from helper import getdriver, getNUI, writeCSV


class Scraper:
    def __init__(self, url, max_workers=5):
        self.url = url
        self.max_workers = max_workers
        
    def get_driver(self):
        return getdriver()

    def load_page(self, driver):
        driver.get(self.url)

    def getNUI(self, code):
        driver = self.get_driver()
        try:
            self.load_page(driver)
            activities = driver.find_element(By.ID, 'ddlnace')
            activities.send_keys(code)
            btnSubmit = driver.find_element(By.ID, 'Submit1')
            btnSubmit.click()
            time.sleep(3)
            driver.maximize_window
            businessNo = driver.find_elements(By.XPATH, '//*[@id="content"]/article/div/table/tbody/tr/td[4]')
            return businessNo
        finally:
            driver.quit()
    
    def scrapeBusiness(self, NUI):
        driver = self.get_driver()
        try:
            self.load_page(driver)
            activities = driver.find_element(By.ID, 'txtNumriBiznesit')
            activities.send_keys(NUI)
            btnSubmit = driver.find_element(By.ID, 'Submit1')
            btnSubmit.click()
            time.sleep(2)
            
            for handle in driver.window_handles:
                driver.switch_to.window(handle)
                
            row = driver.find_element(By.CSS_SELECTOR, 'table.views-table.cols-4 tbody tr td a')
            response = req.get(row.get_attribute('href'))
            soup = BeautifulSoup(response.text, 'lxml')
            business_data_table = soup.select('table.views-table.cols-4')
            business_data = business_data_table[0].select('tbody tr')
            return self.extract_business_data(business_data)
        except Exception as e:
            print(f"Error scraping business {NUI}: {str(e)}")
            return None
        finally:
            driver.quit()

    def extract_business_data(self, business_data):
        name = business_data[0].select('td > span')[0].getText().strip()
        nrbiznesi = business_data[3].select('td > span')[0].getText().strip()
        adresa = business_data[10].select('td > span')[0].getText().strip()
        status = business_data[14].select('td > span')[0].getText().strip()
        phone = business_data[11].select('td > span')[0].getText().strip()
        email = business_data[12].select('td > span')[0].getText().strip()
        return [name, nrbiznesi, status, adresa, phone, email]

    def scrape_batch(self, nui_list):
        results = []
        with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            future_to_nui = {executor.submit(self.scrapeBusiness, nui): nui for nui in nui_list}
            
            for future in as_completed(future_to_nui):
                nui = future_to_nui[future]
                try:
                    data = future.result()
                    if data:
                        results.append(data)
                except Exception as e:
                    print(f"Error processing NUI {nui}: {str(e)}")
        
        return results


def main(fileIn, fileOut):
    NUI = getNUI(fileIn)
    scraper = Scraper("https://arbk.rks-gov.net")
    results = scraper.scrape_batch(NUI)
    for result in results:
        writeCSV(result, fileOut)


def ScrapeNUI(kodi):
    scraper = Scraper("https://arbk.rks-gov.net")
    NUI = scraper.getNUI(kodi)
    writeNUI('NUI.txt', NUI)
    size = len(NUI)
    return size


if __name__ == "__main__":
    
    print("""This program helps you scrape ARBK Business Data based on Activity codes provided.
             Check them out here: https://kk.rks-gov.net/peje/wp-content/uploads/sites/24/2018/05/KODET-veprimtarite.pdf""")
    answer = input("Do you have a dedicated NUI text file with all the businesses you want to scrape? Y/N")

    if answer == 'Y':
       fileName = input("Please make sure the file is in this folder and input the name of the file(with .txt extension)")
       main(fileName, 'Output.csv')
    elif answer == 'N':
        kodi = input("Let's help you with that, write activity code you want to scrape:")
        size = ScrapeNUI(kodi)
        print("You've imported {size} unique business NUI's saved in NUI.txt")
    else: 
        print('Sorry you have to answer with Y or N. Restart the program please.')
        quit()
