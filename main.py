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


# python -m pip install requests

NUI = ''



chrome_options = Options()
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument("--disable-setuid-sandbox")


PATH = "C:/chromedriver.exe"
url = "https://arbk.rks-gov.net"
chrome_driver_path = PATH
driver_service = Service(executable_path=chrome_driver_path)



driver = webdriver.Chrome(service=driver_service)
driver.get(url)
with open('test.txt') as f:
    lines = [line.rstrip('\n') for line in f]
        
for NUI in lines:
    activities = driver.find_element(By.ID, 'txtNumriBiznesit')
    activities.send_keys(NUI)
    btnSubmit = driver.find_element(By.ID, 'Submit1')
    btnSubmit.click()
    time.sleep(3)

    for handle in driver.window_handles:
        driver.switch_to.window(handle)

    row = driver.find_element(
        By.CSS_SELECTOR, 'table.views-table.cols-4 tbody tr td a')

    response = req.get(row.get_attribute('href'))
    soup = BeautifulSoup(response.text, 'lxml')

    business_data_table = soup.select('table.views-table.cols-4')
    business_data = business_data_table[0].select('tbody tr')
    name = business_data[0].select('td > span')[0].getText().strip()
    nrbiznesi = business_data[3].select('td > span')[0].getText().strip()
    status = business_data[14].select('td > span')[0].getText().strip()
    phone  =  business_data[11].select('td > span')[0].getText().strip()
    email = business_data[12].select('td > span')[0].getText().strip()
    info = [name, nrbiznesi, status, phone, email]
    with open('businesses.csv', 'a', encoding='utf-8') as f:
        write = csv.writer(f)
        write.writerow(info)
    time.sleep(2)
driver.quit()
