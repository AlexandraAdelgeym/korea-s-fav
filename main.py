# spotify
import spotipy
from aiogram import types
from spotipy.oauth2 import SpotifyOAuth
from bs4 import BeautifulSoup
import requests



SPOTIPY_CLIENT_ID = "167f663ad2ec4bdbb0b4b0383a181301"
SPOTIPY_CLIENT_SECRET = "ffec7936571a4fc6934be6128e5cb56f"
SPOTIPY_REDIRECT_URI = "http://example.com"

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=SPOTIPY_CLIENT_ID,
                                               client_secret=SPOTIPY_CLIENT_SECRET,
                                               redirect_uri=SPOTIPY_REDIRECT_URI,
                                               cache_path="token.txt",
                                               username="Alexandra"))




user_id = sp.current_user()["id"]

def get_top5():
    response = requests.get("https://www.billboard.com/charts/south-korea-songs-hotw/")

    soup = BeautifulSoup(response.text, 'html.parser')
    song_names_spans = soup.select("li ul li h3")
    artist_names_spans = soup.select("li ul li span")
    song_names = [song.getText().strip() for song in song_names_spans]
    artist_names = [artist.getText().strip() for artist in artist_names_spans]
    new_artist_names = [item for item in artist_names if not item.isdigit()]

    top5 = song_names[:5]
    top5_messages = []

    rate = 1

    for song_name, artist_name in zip(top5, new_artist_names):
        query = f"{song_name} {artist_name}"
        results = sp.search(q=query, type='track', limit=1)
        if results['tracks']['items']:
            track = results['tracks']['items'][0]
            track_name = track['name']
            track_url = track['external_urls']['spotify']
            top5_messages.append(f' {rate}. "{track_name}"  by  {artist_name} <a href="{track_url}">Listen</a>\n')
            rate += 1
        else:
            top5_messages.append("\n")
    return top5_messages
top5_songs = get_top5()


# -----------news--------

def get_top_news():
    response = requests.get("https://www.koreatimes.co.kr/www2/index.asp?ref/")

    soup = BeautifulSoup(response.text, 'html.parser')

    center_container = soup.find('div', class_='top_center_container')
    center_news_titles = [news.getText().strip() for news in center_container if news.getText().strip() != '']
    center_news_links = [link['href'].strip() for link in center_container.find_all('a')]
    # print(center_news_links)

    side_container = soup.find_all('div', class_='top_side_container')
    side_news_titles = set()
    side_news_links = set()

    for element in side_container:
        news_title = element.getText().strip()
        if news_title != '':
            side_news_titles.add(news_title)

        links = element.find_all('a')
        for link in links:
            href = link.get('href', '').strip()
            if href != '':
                side_news_links.add(href)
    side_news_titles = list(side_news_titles)
    side_news_links = list(side_news_links)
    all_titles = center_news_titles + side_news_titles
    all_urls = center_news_links + side_news_links

    top_messages = []
    rate = 1
    for title, url in zip(all_titles, all_urls):
        top_messages.append(f'{rate}. "{title}" <a href="https://www.koreatimes.co.kr/{url}">Read</a>\n')
        rate += 1
    return top_messages

top_news = get_top_news()

#  ----------dramas-----------

def get_top_dramas():
    response = requests.get("https://mydramalist.com/")

    soup = BeautifulSoup(response.text, 'html.parser')
    active_div = soup.find('div', class_='tab-pane active')

    drama_names = active_div.find_all('a', class_='title')
    titles = [drama.getText().strip() for drama in drama_names]
    title_urls =[drama.get('href') for drama in drama_names]
    top_messages = []
    rate = 1
    for title, url in zip(titles, title_urls):
        top_messages.append(f'{rate}. "{title}" <a href="https://mydramalist.com{url}">Watch</a>')
        rate += 1
    return top_messages

top_dramas = get_top_dramas()


#---------learn korean-------
import csv
import random

csv_file_path = 'data/korean_words.csv'
random_pair = None

def get_random_pair():
    global random_pair
    pairs = []
    with open(csv_file_path, 'r', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile)
        next(reader)
        for row in reader:
            korean_word, english_translation = row
            pairs.append((korean_word.strip(), english_translation.strip()))

    random_pair = random.choice(pairs)
    return random_pair




#  ---------bot----------


TELEGRAM_TOKEN = "6554966811:AAGoI6Bey2dfrpSLmTOeBIPoFBhG7YA_-7s"

import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, CallbackQueryHandler

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    start_message = "Hi! \nWhat would you like?"
    keyboard = [
        [InlineKeyboardButton("What's new today?", callback_data='top_things')],
        [InlineKeyboardButton("Learn Korean", callback_data='learn_korean')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await context.bot.send_message(chat_id=update.effective_chat.id, text=start_message, reply_markup=reply_markup)
async def button_click(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    callback_data = query.data

    if callback_data == 'top_things':
        await top_things(update, context)
    elif callback_data == 'learn_korean':
        await learn_korean(update, context)

async def top_things(update: Update, context: ContextTypes.DEFAULT_TYPE):
    combined_message_songs = "\n".join(top5_songs)

    combined_message_dramas = "\n".join(top_dramas)
    combined_message_news = "\n".join(top_news)

    all_messages = (f"Top 5 songs: \n \n{combined_message_songs} \n\nTop dramas: "
                    f"\n \n{combined_message_dramas}\n\nTop news: \n\n{combined_message_news}")

    await context.bot.send_message(chat_id=update.effective_chat.id, text=all_messages,
                                   parse_mode='HTML')

async def learn_korean(update: Update, context: ContextTypes.DEFAULT_TYPE):
    words_pair = get_random_pair()
    message = f"{words_pair[0]}\n{words_pair[1]}"
    await context.bot.send_message(chat_id=update.effective_chat.id, text=message)

if __name__ == '__main__':
    application = ApplicationBuilder().token(TELEGRAM_TOKEN).build()

    start_handler = CommandHandler('start', start)
    application.add_handler(start_handler)

    application.add_handler(CallbackQueryHandler(button_click, pattern='top_things|learn_korean'))



    application.run_polling()


