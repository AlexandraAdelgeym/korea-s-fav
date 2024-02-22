
# spotify
import spotipy
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
            top5_messages.append(f' {rate}. "{track_name}" by {artist_name} <a href="{track_url}">Listen</a>\n')
            rate += 1
        else:
            top5_messages.append("\n")
    return top5_messages
top5_songs = get_top5()
# # news
#
#
# # dramas
#
# bot
TELEGRAM_TOKEN = "6554966811:AAGoI6Bey2dfrpSLmTOeBIPoFBhG7YA_-7s"

import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    combined_message = "\n".join(top5_songs)

    combined_message_with_links = combined_message.replace('[Listen]', '<a href="{track_url}">Listen</a>')

    await context.bot.send_message(chat_id=update.effective_chat.id, text=combined_message_with_links,
                                   parse_mode='HTML')


if __name__ == '__main__':
    application = ApplicationBuilder().token(TELEGRAM_TOKEN).build()

    start_handler = CommandHandler('start', start)
    application.add_handler(start_handler)


    application.run_polling()


