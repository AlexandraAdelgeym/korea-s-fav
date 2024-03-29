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


    for song_name, artist_name in zip(top5, new_artist_names):
        query = f"{song_name} {artist_name}"
        results = sp.search(q=query, type='track', limit=1)
        if results['tracks']['items']:
            track = results['tracks']['items'][0]
            track_name = track['name']
            track_url = track['external_urls']['spotify']
            top5_messages.append(f'🎵  "{track_name}"  by  {artist_name} <a href="{track_url}">Listen</a>\n')
        else:
            top5_messages.append("\n")
    return top5_messages
top5_songs = get_top5()


# -----------news--------
from collections import OrderedDict
def get_top_news():
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
top_news = get_top_news()

# ----------dramas-----------

def get_top_dramas():
    response = requests.get("https://mydramalist.com/")

    soup = BeautifulSoup(response.text, 'html.parser')
    active_div = soup.find('div', class_='tab-pane active')

    drama_names = active_div.find_all('a', class_='title')
    titles = [drama.getText().strip() for drama in drama_names]
    title_urls =[drama.get('href') for drama in drama_names]
    top_messages = []
    for title, url in zip(titles, title_urls):
        top_messages.append(f'🎬  "{title}" <a href="https://mydramalist.com{url}">Watch</a>')
    return top_messages

top_dramas = get_top_dramas()


# #---------learn korean-------
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

def generate_options(correct_translation):
    with open(csv_file_path, 'r', encoding='utf-8') as file:
        reader = csv.reader(file)
        next(reader)
        pairs = [row for row in reader]
        random_pairs = random.sample(pairs, 3)
        options = [pair[1] for pair in random_pairs]
        options.append(correct_translation)
        random.shuffle(options)
        return options


#  ---------bot----------


TELEGRAM_TOKEN = "6554966811:AAGoI6Bey2dfrpSLmTOeBIPoFBhG7YA_-7s"

import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, CallbackQueryHandler
from telegram.ext import MessageHandler, filters

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    start_message = "Hi! \nWhat would you like?"

    keyboard = ReplyKeyboardMarkup([
        [KeyboardButton("🆕 What's new today?")],
        [KeyboardButton("💬 Learn Korean")]
    ], resize_keyboard=True, one_time_keyboard=False)

    reply_markup = keyboard.to_dict()

    await context.bot.send_message(chat_id=update.effective_chat.id, text=start_message, reply_markup=reply_markup)
async def button_click(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    callback_data = query.data

    if callback_data == 'top_things':
        await top_things(update, context)
    elif callback_data == 'learn_korean':
        await learn_korean(update, context)
    elif callback_data.startswith('option_'):
        await handle_option_selection(update, context)


async def top_things(update: Update, context: ContextTypes.DEFAULT_TYPE):
    combined_message_songs = "\n".join(top5_songs)

    combined_message_dramas = "\n".join(top_dramas)
    combined_message_news = "\n".join(top_news)

    all_messages = (f"Top songs: \n \n{combined_message_songs} \n\nTop dramas: "
                    f"\n \n{combined_message_dramas}\n\nTop news: \n\n{combined_message_news}")

    await context.bot.send_message(chat_id=update.effective_chat.id, text=all_messages,
                                   parse_mode='HTML')

current_words_pair = None
correct_translation = None

options = None
async def learn_korean(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global current_words_pair, correct_translation, options
    current_words_pair = get_random_pair()
    correct_translation = current_words_pair[1]

    options = generate_options(correct_translation)
    message = f"Translate the Korean word:\n\n{current_words_pair[0]}"
    reply_markup = InlineKeyboardMarkup([
        [InlineKeyboardButton(options[0], callback_data='option_0')],
        [InlineKeyboardButton(options[1], callback_data='option_1')],
        [InlineKeyboardButton(options[2], callback_data='option_2')],
        [InlineKeyboardButton(options[3], callback_data='option_3')]
    ])
    await context.bot.send_message(chat_id=update.effective_chat.id, text=message, reply_markup=reply_markup)

async def handle_option_selection(update: Update, context: ContextTypes.DEFAULT_TYPE):

    query = update.callback_query
    selected_option_index = int(query.data.split('_')[1])

    if options[selected_option_index] == correct_translation:
        message = "✅ Correct! Next word:"
    else:
        message = f"❌ Wrong! The right answer is: {correct_translation}\nNext word:"

    await context.bot.send_message(chat_id=update.effective_chat.id, text=message)
    await learn_korean(update, context)

async def handle_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text

    if text == "🆕 What's new today?":
        await top_things(update, context)
    elif text == "💬 Learn Korean":
        await learn_korean(update, context)

if __name__ == '__main__':
    application = ApplicationBuilder().token(TELEGRAM_TOKEN).build()

    start_handler = CommandHandler('start', start)
    application.add_handler(start_handler)

    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text))
    application.add_handler(CallbackQueryHandler(button_click, pattern='top_things'))
    application.add_handler(CallbackQueryHandler(button_click, pattern='^learn_korean$|^option_'))





    application.run_polling()


