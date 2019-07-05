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

# Creating loop to open up all divs with same class name
article_list = browser.find_elements_by_css_selector(".views-row.pub1.default-on.clk")

for i in range(0, len(article_list)):
	if article_list[i].is_displayed():
		article_list[i].click() # Getting error: element is not clickable. Refer to: https://stackoverflow.com/questions/37879010/selenium-debugging-element-is-not-clickable-at-point-x-y

# Problem: only 10 articles can be found by css_selector
