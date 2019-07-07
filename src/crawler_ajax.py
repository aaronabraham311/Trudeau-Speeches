import requests
from bs4 import BeautifulSoup

headers = {
    'User-Agent':  'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:69.0) Gecko/20100101 Firefox/69.0'
}


def make_soup(url: str) -> BeautifulSoup:
    res = requests.get(url, headers=headers)
    res.raise_for_status()
    
    return BeautifulSoup(res.text, 'html.parser')


def fetch_speech_details(speech_id: str) -> str:
    url = 'https://pm.gc.ca/eng/views/ajax?view_name=news_article&view_display_id=block&view_args={id}'
    url = url.format(id = speech_id)

    print(url)

    res = requests.get(url, headers=headers)
    res.raise_for_status()

    data = res.json()
    html = data[1]['data']
    soup = BeautifulSoup(html, 'html.parser')

    body = soup.select_one('.views-field-body')
    speech_text = body.get_text()

    return str(speech_text)


def scrape_speeches(soup: BeautifulSoup) -> dict:
    speeches = []
    for teaser in soup.select('.teaser'):
        title = teaser.select_one('.title').text.strip()
        speech_id = teaser['data-nid']
        speech_html = fetch_speech_details(speech_id)
        s = {
            'title': title,
            'details': speech_html
        }
        speeches.append(s)
    return speeches

if __name__ == "__main__":
    url = 'https://pm.gc.ca/eng/news/speeches'
    soup = make_soup(url)
    speeches = scrape_speeches(soup)
    from pprint import pprint
    pprint(speeches)
