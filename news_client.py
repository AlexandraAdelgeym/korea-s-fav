from bs4 import BeautifulSoup
import requests
from collections import OrderedDict


class NewsClient:
    def get_top_news(self):
        response = requests.get("https://www.koreatimes.co.kr/www2/index.asp?ref/")

        soup = BeautifulSoup(response.text, 'html.parser')

        center_container = soup.find('div', class_='top_center_container')
        center_news_titles = [news.getText().strip() for news in center_container if news.getText().strip() != '']
        split_center_news_titles = []
        for title in center_news_titles:
            split_titles = title.split("     ")
            split_titles = [split_title.strip() for split_title in split_titles]
            split_center_news_titles.extend(split_titles)
        center_news_links = [link['href'].strip() for link in center_container.find_all('a', href=True)]

        center_news_links = list(OrderedDict.fromkeys(center_news_links))
        split_center_news_titles = list(OrderedDict.fromkeys(split_center_news_titles))

        upper_titles = []
        upper_links = []
        for article in soup.find_all('article'):
            title_element = article.find('div', class_='top_side_photo_top_headline')
            if title_element:
                title = title_element.a.text.strip()
                href = title_element.a['href']
                upper_titles.append(title)
                upper_links.append(href)
        upper_titles = list(OrderedDict.fromkeys(upper_titles))
        upper_links = list(OrderedDict.fromkeys(upper_links))

        side_titles = []
        side_links = []
        title_element = soup.find_all('div', class_='top_side_sub_headline LoraMedium')
        for element in title_element:
            title = element.a.text
            side_titles.append(title)
            href = element.a['href']
            side_links.append(href)
        side_titles = list(OrderedDict.fromkeys(side_titles))
        side_links = list(OrderedDict.fromkeys(side_links))

        all_titles = split_center_news_titles + upper_titles + side_titles
        all_urls = center_news_links + upper_links + side_links

        final_titles = []
        for title in all_titles:
            if title not in final_titles:
                final_titles.append(title)

        final_links = []
        for link in all_titles:
            if link not in final_links:
                final_links.append(link)

        top_messages = []
        for title, url in zip(final_titles, final_links):
            top_messages.append(f'📰 "{title}" <a href="https://www.koreatimes.co.kr/{url}">Read</a>\n')
        return top_messages

