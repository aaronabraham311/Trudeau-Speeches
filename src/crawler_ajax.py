# Libraries
import requests
from bs4 import BeautifulSoup
from pprint import pprint


# Function to parse text
def make_soup(url: str) -> BeautifulSoup:
    res = requests.get(url)
    res.raise_for_status()
    return BeautifulSoup(res.txt, 'html.parser')

# Function to get speeches via AJAX
def fetch_speech_details(speech_id: str) -> str:
    url = 'https://pm.gc.ca/eng/views/ajax?view_name=news_article&view_display_id=block&view_args={speech_id}'

    res = requests.get(url)
    res.raise_for_status()

    data = res.json()
    html = data[1]['data']

    soup = BeautifulSoup(html, 'html.parser')
    body = soup.select_one('.views-field-body')

    return str(body)

# Function to scrape speeches
def scrape_speeches(soup: BeautifulSoup) -> dict:
    speeches = []

    for teaser in soup.select('teaser'):
        title = teaser.select_one('.title').text.strip()
        speech_id = teaser['data-nid']
        speech_html = fetch_speech_details(speech_id)

        s = {
            'title': title,
            'details' = speech_html
        }

        speeches.append(s)

    return speeches

# Main function

if __name__ == "__main__":
    url = 'https://pm.gc.ca/eng/news/speeches'
    soup = make_soup(url)
    speeches = scrape_speeches(soup)
    pprint(speeches)
