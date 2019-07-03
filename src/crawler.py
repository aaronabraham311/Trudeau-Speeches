# Libraries
from bs4 import BeautifulSoup
#from urllib3.request import urlopen as uReq
import requests

# Opening up connection and grabbing HTML file
my_url = 'https://pm.gc.ca/eng/news/speeches'
page = requests.get(my_url)

page_soup = BeautifulSoup(page.content, "html.parser")

print(page_soup.prettify())
