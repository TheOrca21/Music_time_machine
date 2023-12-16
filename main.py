import requests
import os
from bs4 import BeautifulSoup
import spotipy
from spotipy.oauth2 import SpotifyOAuth

Client_ID = os.environ['spotifyclientid']
Spotify_secret = os.environ['spotifysecret']
date = input("Which year do you want to travel to? Type the date in this format YYYY-MM-DD:")
response = requests.get(f"https://www.billboard.com/charts/hot-100/{date}")
soup = BeautifulSoup(response.text, 'html.parser')
music_list = soup.select('li #title-of-a-story')
titles = [song.getText().strip() for song in music_list]
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope='playlist-modify-private',
                                               redirect_uri='https://example.com',
                                               client_id=Client_ID,
                                               client_secret=Spotify_secret,
                                               show_dialog=True,
                                               cache_path='token.txt',
                                               username='sudhakar'))
user_id = sp.current_user()['id']
song_uris = []
year = date.split('-')[0]
for song in titles:
    result = sp.search(q=f'track:{song} year:{year}', type='track')
    print(result)
    try:
        uri = result['tracks']['items'][0]['uri']
        song_uris.append(uri)
    except IndexError:
        print(f"{song} not found in spotify!")
playlist = sp.user_playlist_create(user=user_id, name=f"{date} Billboard 100", public=False)
sp.playlist_add_items(playlist_id=playlist['id'], items=song_uris)
