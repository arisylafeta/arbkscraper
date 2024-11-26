from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager
import csv
import pandas as pd
import os

def writeNUI(fileName, NUI):
    with open(fileName, 'w') as f:
        for numer in NUI:
            f.write(f"{numer.text}\n")

def getdriver():
    chrome_options = Options()
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--headless')  # Run in headless mode (optional)
    chrome_options.add_argument('--disable-dev-shm-usage')
    
    driver = webdriver.Chrome(
        service=Service(ChromeDriverManager().install()),
        options=chrome_options
    )
    return driver

#Get NUI from textfile
def getNUI(fileName):
    with open(fileName) as f:
        lines = [line.rstrip('\n') for line in f]
    return lines


#Write data to file
def writeCSV(info, fileName):
    with open(fileName, 'a', encoding='utf-8', newline='') as f:
        write = csv.writer(f)
        write.writerow(info)
