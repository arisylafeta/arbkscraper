from bs4 import BeautifulSoup
import requests as req
from selenium import webdriver
import time
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import lxml

PATH = "C:/chromedriver.exe"
url = "https://arbk.rks-gov.net"
chrome_driver_path = PATH
driver_service = Service(executable_path=chrome_driver_path)

driver = webdriver.Chrome(service=driver_service)
driver.get(url)
activities = driver.find_element(By.ID, 'ddlnace')
activities.send_keys('4120')
btnSubmit = driver.find_element(By.ID, 'Submit1')
btnSubmit.click()

time.sleep(5)
driver.maximize_window
businessNo= driver.find_elements(By.XPATH, '//*[@id="content"]/article/div/table/tbody/tr/td[4]')

with open('numrat.txt', 'w') as f:
    for business in businessNo:
        f.write(f"{business.text}\n")