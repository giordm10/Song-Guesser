# Guess That Song!
## A little bit about our Game!

This is our song guessing game! During the game players will be able to choose an artist and then they will listen to a song where they can type in a title to try and guess the song. If the player is correct they will get a point, otherwise they will not. Play one player to try and get on the leaderboard, or play with a friend in 2 player mode to try and beat them. If playing with someone that is blind or vison impaired, turn on text to speech mode in settings to have our game talk to you!

## This package contains

game.py - runs main pygame loop

album_cover_mappings.py - maps song name to associated album cover, used in game.py

spotipy_artist.py - gets song preview URLs from an artist on spotify, uses spotipy, used in game.py

musicplayer.py - used to play songs in the program as well as text to voice. used in game.py

speechFiles/ - where all the speech files used in text to speech are located

images/ - where the album cover images are stored

leaderboard.csv - where leaderboard values are stored

## Packages needed

### PIP packages needed:

pygame 2.1.2

pygame_textinput 1.0.1

spotipy 2.21.0

requests 2.28.1

python-dotenv 0.21.0

### Other packages:

mpg123 1.31.1

## Additional Information

Tested on python version 3.10.8 but may work on others

The program needs internet access to work


## How to Run

Navigate to the directory in a terminal where all files are located, and type

$ python game.py
