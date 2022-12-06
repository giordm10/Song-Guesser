import argparse
import logging

from spotipy.oauth2 import SpotifyClientCredentials
import spotipy
from dotenv import load_dotenv

load_dotenv()

logger = logging.getLogger('examples.artist_albums')
logging.basicConfig(level='INFO')

sp = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials())

#Used when this file is called directly from the command line
def get_args():
    parser = argparse.ArgumentParser(description='Gets albums from artist')
    parser.add_argument('-a', '--artist', required=True,
                        help='Name of Artist')
    return parser.parse_args()

#returns the most popular artist with a given name - for example there are multiple artists named Michael Jackson but this function will return the most famous Michal Jackson (ie the one that sang songs such as Beat It! and Billie Jean)
def get_artist(name):
    results = sp.search(q='artist:' + name, type='artist')
    items = results['artists']['items']
    if len(items) > 0:
        return items[0]
    else:
        return None

#Uses spotify api to retrieve their top 10 most popular songs
#returns a dictionary of pairs of (song name, preview url)
def show_artist_top_tracks(artist):
    results = sp.artist_top_tracks(artist['id'], country="US")
    results2 = results['tracks']
    songDict = {}
    for songIterable in range(0,len(results2)):
        songDict[results2[songIterable]["name"]] = results2[songIterable]["preview_url"]

        #Used to retrieve album covers
        # print(results2[songIterable]["name"])
        # print(results2[songIterable]["album"]["images"])
        # print()

        #Used to check if artist has 10 songs that have preview urls
        # print(results2[songIterable]["name"] + " - " + results2[songIterable]["preview_url"])
    return songDict

#Users can call this function directly with "python3 spotipy_artist.py -a "NAME OF ARTIST" This will run this file directly without using the game
#Can be useful to check if artist exists, if they have preview_urls or to retrieve other information like album covers
#This feature is only useful in development mode
def main():
    args = get_args()
    artist = get_artist(args.artist)
    if artist:
        show_artist_top_tracks(artist)
    else:
        logger.error("Can't find artist: %s", artist)


if __name__ == '__main__':
    main()