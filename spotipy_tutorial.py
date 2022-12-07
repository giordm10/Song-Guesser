import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from dotenv import load_dotenv

load_dotenv()
#SPOTIPY_CLIENT_ID='914edfe2387b4fdb9de4fcd942faed5b'
#SPOTIPY_CLIENT_SECRET='43d99df3213b4de2b190f8aa8602eb65'
#SPOTIPY_REDIRECT_URI='https://localhost:8888/callback'

birdy_uri = 'spotify:artist:2WX2uTcsvV5OnS0inACecP'
spotify = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials())

results = spotify.artist_albums(birdy_uri, album_type='album')
albums = results['items']
while results['next']:
    results = spotify.next(results)
    albums.extend(results['items'])

for album in albums:
    print(album['name'])