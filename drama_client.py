import requests
from bs4 import BeautifulSoup

class DramaClient:
    def get_top_dramas(self):
        response = requests.get("https://mydramalist.com/")

        soup = BeautifulSoup(response.text, 'html.parser')
        active_div = soup.find('div', class_='tab-pane active')

        drama_names = active_div.find_all('a', class_='title')
        titles = [drama.getText().strip() for drama in drama_names]
        title_urls = [drama.get('href') for drama in drama_names]
        top_messages = []
        for title, url in zip(titles, title_urls):
            top_messages.append(f'🎬  "{title}" <a href="https://mydramalist.com{url}">Watch</a>')
        return top_messages
