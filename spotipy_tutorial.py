import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from dotenv import load_dotenv

load_dotenv()
#SPOTIPY_CLIENT_ID='914edfe2387b4fdb9de4fcd942faed5b'
#SPOTIPY_CLIENT_SECRET='43d99df3213b4de2b190f8aa8602eb65'
#SPOTIPY_REDIRECT_URI='https://localhost:8888/callback'

# import spotipy
# from spotipy.oauth2 import SpotifyClientCredentials

lz_uri = 'spotify:artist:36QJpDe2go2KgaRleHCDTp'

spotify = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials())
results = spotify.artist_top_tracks(lz_uri)

for track in results['tracks'][:10]:
    print('track    : ' + track['name'])
    print('audio    : ' + track['preview_url'])
    print('cover art: ' + track['album']['images'][0]['url'])
    print()