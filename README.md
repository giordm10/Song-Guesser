# Guess That Song!
game.py - runs main pygame loop

album_cover_mappings.py - maps song name to associated album cover, used in game.py

spotipy_artist.py - gets song preview URLs from an artist on spotify, uses spotipy, used in game.py

musicplayer.py - used to play songs in the program as well as text to voice. used in game.py

speechFiles/ - where all the speech files used in text to speech are located

images/ - where the album cover images are stored

leaderboard.csv - where leaderboard values are stored


PIP packages needed:

pygame 2.1.2

pygame_textinput 1.0.1

spotipy 2.21.0

requests 2.28.1

python-dotenv 0.21.0


Tested on python version 3.10.8 but may work on others

The program needs internet access to work

To run the program, type in a terminal

$ python game.py
