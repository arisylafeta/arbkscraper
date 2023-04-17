from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
import csv

def writeNUI(fileName, NUI):
    with open(fileName, 'w') as f:
        for numer in NUI:
            f.write(f"{numer.text}\n")

#Get driver 
def getdriver():
    chrome_options = Options()
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument("--disable-setuid-sandbox")
    PATH = "C:/chromedriver.exe"
    chrome_driver_path = PATH
    driver_service = Service(executable_path=chrome_driver_path)
    driver = webdriver.Chrome(service=driver_service, options=chrome_options)
    return driver


#Get NUI from textfile
def getNUI(fileName):
    with open(fileName) as f:
        lines = [line.rstrip('\n') for line in f]
    return lines


#Write data to file
def writeCSV(info, fileName):
    with open(fileName, 'a', encoding='utf-8') as f:
        write = csv.writer(f)
        write.writerow(info)