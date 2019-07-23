# Libraries
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import requests
import time

# Opening up connection and grabbing HTML file via Chrome
url = 'https://pm.gc.ca/eng/news/speeches'
browser = webdriver.Chrome()
browser.get(url)

# Delaying scrapper to prevent scrapper from closing too soon
browser.implicitly_wait(2)

'''
while True:
    try:
        element = browser.find_element_by_xpath('//*[@id="block-system-main"]/div/ul/li/a')
        element.click()
    except:
        break
'''

wait = WebDriverWait(browser, 10)
i = 0
while True:
    i += 1
    try:

        if i == 1:
            print("Trying to click ")
            element = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="block-system-main"]/div/ul/li/a')))
            element.click()
        else:
            xpath = '//*[@id="block-system-main"]/div[{pagenum}]/ul/li/a'
            xpath = xpath.format(pagenum = i)
            print(xpath)
            element = wait.until(EC.element_to_be_clickable((By.XPATH, xpath)))
            element.click()
    except:
        break