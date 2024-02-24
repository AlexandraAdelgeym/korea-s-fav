import spotipy
from spotipy.oauth2 import SpotifyOAuth
import requests
from bs4 import BeautifulSoup

class SpotifyClient:
    def __init__(self, client_id, client_secret, redirect_uri, username):
        self.sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
            client_id=client_id,
            client_secret=client_secret,
            redirect_uri=redirect_uri,
            cache_path="token.txt",
            username=username
        ))
        self.user_id = self.sp.current_user()["id"]

    def get_top5(self):
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
            results = self.sp.search(q=query, type='track', limit=1)
            if results['tracks']['items']:
                track = results['tracks']['items'][0]
                track_name = track['name']
                track_url = track['external_urls']['spotify']
                top5_messages.append(f'🎵  "{track_name}"  by  {artist_name} <a href="{track_url}">Listen</a>\n')
            else:
                top5_messages.append("\n")
        return top5_messages
