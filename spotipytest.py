import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from spotipy.oauth2 import SpotifyOAuth
from dotenv import load_dotenv
from pprint import pprint
from time import sleep

load_dotenv()
#SPOTIPY_CLIENT_ID='914edfe2387b4fdb9de4fcd942faed5b'
#SPOTIPY_CLIENT_SECRET='43d99df3213b4de2b190f8aa8602eb65'
#SPOTIPY_REDIRECT_URI='https://localhost:8888/callback'

scope = "user-read-playback-state,user-modify-playback-state"
sp = spotipy.Spotify(client_credentials_manager=SpotifyOAuth(scope=scope))

# Shows playing devices
res = sp.devices()
pprint(res)

# Change track
sp.start_playback(uris=['spotify:track:6gdLoMygLsgktydTQ71b15'])

# Change volume
sp.volume(100)
sleep(2)
sp.volume(50)
sleep(2)
sp.volume(100)
