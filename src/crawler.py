# Libraries
from bs4 import BeautifulSoup
from selenium import webdriver
import requests
import os

# Opening up connection and grabbing HTML file via Chrome
url = 'https://pm.gc.ca/eng/news/speeches'
browser = webdriver.Chrome()
browser.get(url)

html = browser.page_source
print(html)
