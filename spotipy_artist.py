import argparse
import logging

from spotipy.oauth2 import SpotifyClientCredentials
import spotipy
from dotenv import load_dotenv

load_dotenv()

logger = logging.getLogger('examples.artist_albums')
logging.basicConfig(level='INFO')

sp = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials())


def get_args():
    parser = argparse.ArgumentParser(description='Gets albums from artist')
    parser.add_argument('-a', '--artist', required=True,
                        help='Name of Artist')
    return parser.parse_args()


def get_artist(name):
    results = sp.search(q='artist:' + name, type='artist')
    items = results['artists']['items']
    if len(items) > 0:
        return items[0]
    else:
        return None


# def show_artist_albums(artist):
#     albums = []
#     results = sp.artist_albums(artist['id'], album_type='album')
#     print(results)
#     albums.extend(results['items'])
#     while results['next']:
#         results = sp.next(results)
#         albums.extend(results['items'])
#     seen = set()  # to avoid dups
#     albums.sort(key=lambda album: album['name'].lower())
#     for album in albums:
#         name = album['name']
#         if name not in seen:
#             logger.info('ALBUM: %s', name)
#             seen.add(name)

def show_artist_top_tracks(artist):
    results = sp.artist_top_tracks(artist['id'], country="US")
    # print(results)
    results2 = results['tracks']
    for songIterable in range(0,len(results2)):
        print(results2[songIterable]["name"] + " - " + results2[songIterable]["preview_url"])
        # print(len(results2))
        # results3 = results2[songIterable]["album"]
        # print(results3)
        # results4 = results3["name"]
        # print(results4)
    # songs.extend(results['tracks'])
    # while results['next']:
    #     results = sp.next(results)
    #     songs.extend(results['items'])
    # seen = set()  # to avoid dups
    # songs.sort(key=lambda album: album['name'].lower())
    # for album in songs:
    #     name = album['name']
    #     if name not in seen:
    #         logger.info('ALBUM: %s', name)
    #         seen.add(name)

def main():
    args = get_args()
    artist = get_artist(args.artist)
    if artist:
        show_artist_top_tracks(artist)
    else:
        logger.error("Can't find artist: %s", artist)


if __name__ == '__main__':
    main()