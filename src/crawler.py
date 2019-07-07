# Libraries
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import requests
import time

# Opening up connection and grabbing HTML file via Chrome
url = 'https://pm.gc.ca/eng/news/speeches'
browser = webdriver.Chrome()
browser.get(url)

# Delaying scrapper to prevent scrapper from closing too soon
browser.implicitly_wait(2)

# Creating loop to open up all divs with same class name
article_list = browser.find_elements_by_css_selector(".views-row.pub1.default-on.clk")

# All titles for expanded divs printed. Works!
for article in article_list:
	print(article.text)


# Only works for first article in list
for article in article_list:
	article.click()
	
	time.sleep(3)
	
	# Getting title
	title = article.find_element_by_xpath("//h1[@class = 'field-content']")
	print(title.text)	

	# Getting date
	date = article.find_element_by_class_name("date-display-single")
	print(date.text)

	# Getting place
	place = article.find_element_by_xpath("//div[@class = 'inline-date']")
	print(place.text)

	# Getting speech
	speech_div = browser.find_elements_by_xpath("//span[@lang = 'EN-CA']")
	
	for p in speech_div:
		print(p.text)
