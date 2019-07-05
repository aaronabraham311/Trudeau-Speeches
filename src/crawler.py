# Libraries
from bs4 import BeautifulSoup
from selenium import webdriver
import requests
import time

# Opening up connection and grabbing HTML file via Chrome
url = 'https://pm.gc.ca/eng/news/speeches'
browser = webdriver.Chrome()
browser.get(url)

# Delaying scrapper to prevent scrapper from closing too soon
time.sleep(2)

# Parsing the data via bs4
html = browser.page_source
soup = BeautifulSoup(html, 'html.parser')

# Saving initial raw soup
with open('../data/scrapped.txt', 'w') as file:
	file.write(str(soup))

# Clicking a speech box
browser.find_element_by_css_selector(".views-row.views-row-1.pub1.default-on.clk").click()

