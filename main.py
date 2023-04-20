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

def ScrapeNUI(kodi):
    scraper = Scraper("https://arbk.rks-gov.net")
    scraper.load_page()
    NUI = scraper.getNUI(kodi)
    writeNUI('NUI.txt', NUI)
    scraper.close_driver()
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


#######################BONUS FUNCTIONALITY FOR HARDCORE USERS#########################################
"""
    If you have more than 1000 NUI's the second step of this program takes a long time to scrape, therefore, its recommended to use multiprocessing to parallel work.
    BEWARE THIS MIGHT HEAVILY EXHAUST YOUR COMPUTER's RESOURCES AND CAN LEAD TO WINDOWS ERRORS, I RECOMMEND NOT USING MORE THAN 4 THREADS. 

    #Simply spread out your NUI's evenly in 4 different text files, and copy and paste the code below inside the second if condition "elif answer ==N:"

    #Make sure to create 4 input files and output files with the same names on your directory
    fileIn = ['input.txt', 'input1.txt', 'input2.txt', 'input3.txt']
    fileOut = ['output.csv','output1.csv', 'output2.csv', 'output3.csv']

    processList = []

    with ProcessPoolExecutor() as executor:
        for num in range(len(fileIn)):
            processList.append(executor.submit(main, fileIn[num], fileOut[num]))

    wait(processList)

    print("Scraping finished...")

"""
    


