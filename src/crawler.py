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

for article in article_list:
	article.click()
	time.sleep(1)

	# Getting date
	date = browser.find_element_by_class_name("date-display-single")
	print(date.text)

	# Getting place
	place = browser.find_element_by_xpath("//div[@class = 'inline-date']")
	print(place.text)

	# Getting speech
	speech_div = browser.find_elements_by_xpath("//span[@lang = 'EN-CA']")
	
	for p in speech_div:
		print(p.text)
	
	

# Problem: only 10 articles can be found by css_selector
