import time
import tkinter as tk
import csv
import lxml
import requests as req
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from concurrent.futures import ProcessPoolExecutor, wait
from helper import getdriver, getNUI, writeNUI, writeCSV
# python -m pip install requests


class Scraper:
    def __init__(self, url):
        self.url = url
        self.driver = getdriver()

    def load_page(self):
        self.driver.get(self.url)

    def getNUI(self, code):
        activities = self.driver.find_element(By.ID, 'ddlnace')
        activities.send_keys(code)
        btnSubmit = self.driver.find_element(By.ID, 'Submit1')
        btnSubmit.click()
        time.sleep(3)
        self.driver.maximize_window
        businessNo= self.driver.find_elements(By.XPATH, '//*[@id="content"]/article/div/table/tbody/tr/td[4]')
        return businessNo
    
    #Get Business data from NUI
    def scrapeBusiness(self, NUI):
        driver = self.driver
        activities = driver.find_element(By.ID, 'txtNumriBiznesit')
        activities.send_keys(NUI)
        btnSubmit = driver.find_element(By.ID, 'Submit1')
        btnSubmit.click()
        time.sleep(2)
        for handle in driver.window_handles:
            driver.switch_to.window(handle)
        row = driver.find_element(
            By.CSS_SELECTOR, 'table.views-table.cols-4 tbody tr td a')
        response = req.get(row.get_attribute('href'))
        soup = BeautifulSoup(response.text, 'lxml')
        business_data_table = soup.select('table.views-table.cols-4')
        business_data = business_data_table[0].select('tbody tr')

        #Can add more data types depending on needs. 
        name = business_data[0].select('td > span')[0].getText().strip()
        nrbiznesi = business_data[3].select('td > span')[0].getText().strip()
        adresa = business_data[10].select('td > span')[0].getText().strip()
        status = business_data[14].select('td > span')[0].getText().strip()
        phone  =  business_data[11].select('td > span')[0].getText().strip()
        email = business_data[12].select('td > span')[0].getText().strip()
        info = [name, nrbiznesi, status, adresa, phone, email]
        return info
    
    def close_driver(self):
        self.driver.close()

    
def main(fileIn, fileOut):
    NUI = getNUI(fileIn)
    scraper = Scraper("https://arbk.rks-gov.net")
    scraper.load_page()
    for numer in NUI:
        data = scraper.scrapeBusiness(numer)
        writeCSV(data, fileOut)
    scraper.close_driver()

if __name__ == "__main__":
    
    fileIn= ['test.txt', 'test1.txt', 'test2.txt', 'test3.txt']
    fileOut = ['test.csv', 'test1.csv', 'test2.csv', 'test3.csv']

    processList = []

    with ProcessPoolExecutor() as executor:
        for num in range(len(fileIn)):
            processList.append(executor.submit(main, fileIn[num], fileOut[num]))

    wait(processList)

