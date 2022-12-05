"""
main game file for Song-Guesser Game
runs the pygame loop
Developed by BBMJ
"""

#import packages
import pygame
import pygame_textinput
import sys
import spotipy
import re
import lb
import spotipy_artist
import webbrowser
import random
import os
import musicplayer
import album_cover_mappings
import requests

#headers for requests when downloading the songs
headers = {
    'Host': 'p.scdn.co',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.5',
    'DNT': '1',
    'Upgrade-Insecure-Requests': '1',
    'Sec-Fetch-Dest': 'document',
    'Sec-Fetch-Mode': 'navigate',
    'Sec-Fetch-Site': 'none',
    'Sec-Fetch-User': '?1',
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:107.0) Gecko/20100101 Firefox/107.0',
}


# initializing the game, setting window title
pygame.init()
clock = pygame.time.Clock()
pygame.display.set_caption('Guess That Song')

#make textbox
textinput = pygame_textinput.TextInputVisualizer()
textinput.font_color = (255, 255, 255)
textinput.cursor_color = (255, 255, 255)
pygame.key.set_repeat(500, 50) # allow user to hold down key and detect it

#inital variables / set game running
running = True
state = "mainMenu"
firstGuess = True
  
# game resolution
res = (1280,720)
  
# set window to specified resolution
gameDisplay = pygame.display.set_mode(res)
  
# define color
white = (255,255,255)
  
# light shade of the button
color_light = (170,170,170)
  
# dark shade of the button
color_dark = (100,100,100)
  
# defining three font sizes
smallerfont = pygame.font.SysFont('Corbel',18)
smallfont = pygame.font.SysFont('Corbel',35)
largefont = pygame.font.SysFont('Corbel',80)
  
  
#flag for only opening tab once
song_open = False

#flag to see if list is generated
list_generated = False

#information/variables used during the gameplay of program
curr_artist = ""
songLink = ""
songDict = {}
score = 0
scorePlayer2 = 0
turn = 1 #inital player for 2 player
leaderboardInformation = False
infoDict = dict()
leaderboardNameEntered = False
onePlayerMode = True
textToSpeechEnabled = False #if text to speech is enabled
onlyGuess = False #variable so user can only guess once

#Variables utilized in controlling execution of text to speech for on-screen instructions and output
onePlayerInstructionsSpoke = False
twoPlayerInstructionsSpoke = False
guessInstructionsSpoke = False
correctGuessSpoke = False
incorrectGuessSpoke = False
turnSpoke = False
gameOverSpoke = False
winnerSpoke = False

#initalize player to play songs as well as for text to speech
speechPlayer = musicplayer.MusicPlayer()
musicPlayer = musicplayer.MusicPlayer()

"""
button function - displays a button in the game
parameters:
#x - x coordinate of button
#y - y coordinate of button
#w - width of button
#h - height of button
#ic - unhighlighted color
#ac - highlighted color
#artist - if the button is selecting an artist
#action - action (function) on button click. can be a string of a state, or name of a function
#mp3 - specified mp3 file to play when the user hovers on the button if text to speech is enabled
"""
def button(msg,x,y,w,h,ic,ac,events, artist=None, action=None, mp3=None):
    clicked = False
    global curr_artist
    global textToSpeech
    for event in events:
        if event.type == pygame.MOUSEBUTTONDOWN:
            clicked = True
    global state
    played = False
    mouse = pygame.mouse.get_pos()
    if x+w > mouse[0] > x and y+h > mouse[1] > y: #if mouse hovered over
        pygame.draw.rect(gameDisplay, ac,(x,y,w,h))
        if(textToSpeechEnabled == True and action != "textToSpeech" and not speechPlayer.is_playing()):
            speechPlayer.play(os.path.join('speechFiles', mp3))
        if clicked and action != None: #if clicked
            if artist != None: 
                curr_artist = artist #set artist if specified
            if isinstance(action, str) == True:
                state = action #set state to action if a string is speciied
            else:
                action() #call method if the action is a method
    else: #else mouse not hovered over
        pygame.draw.rect(gameDisplay, ic,(x,y,w,h))
    if artist == None:
        text = smallfont.render(msg , True , white)
    else:
        text = smallerfont.render(msg , True , white)
    gameDisplay.blit(text, ( (x+(w/5.5)), (y+(h/3)) )) #display the text on the button

#starts the game
def start():
    loop()
    end()

"""
main game loop
calls associated state depedent on current state
"""
def loop():
    #use game variabls and global variables
    global state 
    global running
    global song_open
    global list_generated
    global curr_artist
    global score
    global scorePlayer2
    global turn
    global firstGuess
    global leaderboardNameEntered
    global onePlayerMode
    global textToSpeechEnabled
    global onlyGuess
    global songLink
    global correctGuessSpoke
    global incorrectGuessSpoke
    global turnSpoke
    scoreFlag = False
    running = True
    result = ""
    songDict = ""
    text = ""
    correctAnswer = None
    while running:
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                loop = False
                end()
        render()
        
        #check state and call associated method
        #each method passes in even
        if state == "mainMenu": #mainMenu state (initial state of the game)
            mainMenu(events)
        elif state == "settingsMenu": #settings state
            setting(events)
        elif state == "leaderboard": #leaderboard state
            leaderboard(events)
        elif state == "onePlayer": #1 player option selected, bring to artist selection
            score = 0
            leaderboardNameEntered = False
            onePlayerMode = True
            onePlayer(events)
        elif state == "twoPlayer": #2 player option selected, bring to artist selection
            score = 0
            scorePlayer2 = 0
            turn = 1
            leaderboardNameEntered = False
            onePlayerMode = False
            twoPlayer(events)
        elif state == "gameOver": #game over state
            gameOver(events)
            firstGuess = True
            for event in events:
                if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN and leaderboardNameEntered == False:
                    updateLeaderboard()
                    leaderboardNameEntered = True
        elif state == "endGame": #end game state when clicked
            list_generated = False
            textinput.value = ""
            curr_artist = ""
            songLink = ""
            onlyGuess = False
            song_open = False
            correctAnswer = None
            state = "gameOver"
            
        elif state == "randomSong": #when state is in 1 player game
            if(firstGuess):
                firstGuess = False
                textinput.value = ""
            if(not list_generated):
                result = spotipy_artist.get_artist(curr_artist)
                songDict = spotipy_artist.show_artist_top_tracks(result)
                list_generated = True
            if(not song_open and len(songDict) != 0):
                num_options = len(songDict) - 1
                randomNum = random.randint(0,num_options)
                songTitle = list(songDict)[randomNum]
                songLink = list(songDict.values())[randomNum]
                text = smallfont.render("Type the name of the song and click the \"Enter\" key.    Score: " + str(score), True , white)
                response = requests.get(str(songLink), headers=headers)
                with open('song.mp3', 'wb') as f:
                    f.write(response.content)
                if(not musicPlayer.is_playing()):
                    musicPlayer.play("song.mp3")
                del songDict[songTitle]
                scoreFlag = False
                song_open = True
            if onlyGuess == True:
                getAlbumnCover(songTitle)
            
            for event in events:
                if re.sub('[^A-Za-z0-9]+', '', textinput.value.lower()) == re.sub('[^A-Za-z0-9]+', '', songTitle.lower()) and event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                    onlyGuess = True
                    if(not scoreFlag):
                        score += 1
                        scoreFlag = True
                    text = smallfont.render("Correct Guess!    Score: " + str(score) , True , white)
                    correctGuessHasPlayed = False #the correct guess mp3 has played so the score mp3 can play
                    if(textToSpeechEnabled == True):
                        while(correctGuessSpoke == False):
                            if(correctGuessHasPlayed == False and not speechPlayer.is_playing()):
                                speechPlayer.play(os.path.join('speechFiles', 'correctguess.mp3'))
                                correctGuessHasPlayed = True
                            if(correctGuessHasPlayed == True and not speechPlayer.is_playing()):
                                speechPlayer.play(os.path.join('speechFiles', 'playeronescore'+ str(score) + '.mp3'))
                                correctGuessSpoke = True
                elif textinput.value.lower() != songTitle.lower() and event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                    onlyGuess = True
                    text = smallfont.render("Incorrect Guess!   Score: " + str(score) , True , white)
                    correctAnswer = smallfont.render("The correct guess was: " + songTitle, True , white)
                    incorrectGuessHasPlayed = False #the incorrect guess mp3 has played so the score mp3 can play
                    if(textToSpeechEnabled == True):
                        while(incorrectGuessSpoke == False):
                            if(incorrectGuessHasPlayed == False and not speechPlayer.is_playing()):
                                speechPlayer.play(os.path.join('speechFiles', 'incorrectguess.mp3'))
                                incorrectGuessHasPlayed = True
                            if(incorrectGuessHasPlayed == True and not speechPlayer.is_playing()):
                                speechPlayer.play(os.path.join('speechFiles', 'playeronescore'+ str(score) + '.mp3'))
                                incorrectGuessSpoke = True
            if correctAnswer is not None:
                 randomSong(events, text, correctAnswer)
            else:
                 randomSong(events, text)
            

        elif state == "randomSong2": #when state is in 2 player gamme
            if(firstGuess):
                firstGuess = False
                textinput.value = ""
            if(not list_generated):
                result = spotipy_artist.get_artist(curr_artist)
                songDict = spotipy_artist.show_artist_top_tracks(result)
                list_generated = True
            if(not song_open and len(songDict) != 0):
                num_options = len(songDict) - 1
                randomNum = random.randint(0,num_options)
                songTitle = list(songDict)[randomNum]
                songLink = list(songDict.values())[randomNum]
                text = smallfont.render("Type the name of the song and click the \"Enter\" key.    Player 1 Score: " + str(score) + ", Player 2 Score: " + str(scorePlayer2), True , white)
                player1Turn = smallfont.render("Player 1's turn", True, white)
                player2Turn = smallfont.render("Player 2's turn", True, white)
                if turn == 1:
                    turnText = player1Turn
                    turnTalk = "playeroneturn.mp3"
                elif turn == 2:
                    turnText = player2Turn
                    turnTalk = "playertwoturn.mp3"
                response = requests.get(str(songLink), headers=headers)
                with open('song.mp3', 'wb') as f:
                    f.write(response.content)
                if(not musicPlayer.is_playing()):
                    musicPlayer.play("song.mp3")
                del songDict[songTitle]
                scoreFlag = False
                song_open = True
            if onlyGuess == True:
                getAlbumnCover(songTitle)

            for event in events:
                if re.sub('[^A-Za-z0-9]+', '', textinput.value.lower()) == re.sub('[^A-Za-z0-9]+', '', songTitle.lower()) and event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                    onlyGuess = True
                    if turn == 1:
                        if(not scoreFlag):
                            scoreFlag = True
                            score += 1
                    elif turn == 2:
                        if(not scoreFlag):
                            scoreFlag = True
                            scorePlayer2 +=1
                    text = smallfont.render("Correct Guess!    Player 1 Score: " + str(score) + ", Player 2 Score: " + str(scorePlayer2), True , white)
                    correctGuessHasPlayed = False #the correct guess mp3 has played so the score mp3s can play
                    playerOneScorePlayed = False #player one's score mp3 has played so player two's score mp3 can play
                    if(textToSpeechEnabled == True):
                        while(correctGuessSpoke == False):
                            if(correctGuessHasPlayed == False and not speechPlayer.is_playing()):
                                speechPlayer.play(os.path.join('speechFiles', 'correctguess.mp3'))
                                correctGuessHasPlayed = True
                            if(correctGuessHasPlayed == True and not speechPlayer.is_playing() and playerOneScorePlayed == False):
                                speechPlayer.play(os.path.join('speechFiles', 'playeronescore'+ str(score) + '.mp3'))
                                playerOneScorePlayed = True
                            if(playerOneScorePlayed == True and not speechPlayer.is_playing()):
                                speechPlayer.play(os.path.join('speechFiles', 'playertwoscore'+ str(scorePlayer2) + '.mp3'))
                                correctGuessSpoke = True
                elif textinput.value.lower() != songTitle.lower() and event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                    onlyGuess = True
                    text = smallfont.render("Incorrect Guess!   Player 1 Score: " + str(score) + ", Player 2 Score: " + str(scorePlayer2), True , white)
                    correctAnswer = smallfont.render("The correct guess was: " + songTitle, True , white)
                    incorrectGuessHasPlayed = False #the incorrect guess mp3 has played so the score mp3s can play
                    playerOneScorePlayed = False #player one's score mp3 has played so player two's score mp3 can play
                    if(textToSpeechEnabled == True):
                        while(incorrectGuessSpoke == False):
                            if(incorrectGuessHasPlayed == False and not speechPlayer.is_playing()):
                                speechPlayer.play(os.path.join('speechFiles', 'incorrectguess.mp3'))
                                incorrectGuessHasPlayed = True
                            if(incorrectGuessHasPlayed == True and not speechPlayer.is_playing() and playerOneScorePlayed == False):
                                speechPlayer.play(os.path.join('speechFiles', 'playeronescore'+ str(score) + '.mp3'))
                                playerOneScorePlayed = True
                            if(playerOneScorePlayed == True and not speechPlayer.is_playing()):
                                speechPlayer.play(os.path.join('speechFiles', 'playertwoscore'+ str(scorePlayer2) + '.mp3'))
                                incorrectGuessSpoke = True
                    if turn == 1:
                        turn = 2
                    elif turn == 2:
                        turn = 1
            if correctAnswer is not None:
                 randomSong2(events, text, turnText, turnTalk, correctAnswer)
            else:
                 randomSong2(events, text, turnText, turnTalk)
        elif state == "nextSong": #next song button in 1 player mode
            correctAnswer = None
            gameDisplay.blit(smallfont.render("Downloading song...", True , white), ((0+(50/2)), (100+(50/2))))
            if(musicPlayer.is_playing()):
                musicPlayer.quit_playing()
            textinput.value = ""
            clock.tick(30)
            song_open = False
            pygame.mouse.set_pos(150, 419)
            if(len(songDict) == 0):
                list_generated = False
                state = "gameOver"
            else:
                onlyGuess = False
                correctGuessSpoke = False
                incorrectGuessSpoke = False
                state = "randomSong"
        elif state == "nextSong2": #next song buttton in 2 player mode
            correctAnswer = None
            gameDisplay.blit(smallfont.render("Downloading song...", True , white), ((0+(50/2)), (100+(50/2))))
            if(musicPlayer.is_playing()):
                musicPlayer.quit_playing()
            canPlay = False
            textinput.value = ""
            clock.tick(30)
            song_open = False
            if turn == 1:
                turn = 2
            elif turn == 2:
                turn = 1
            pygame.mouse.set_pos(150, 419)
            if(len(songDict) == 0):
                list_generated = False
                state = "gameOver"
            else:
                onlyGuess = False
                correctGuessSpoke = False
                incorrectGuessSpoke = False
                turnSpoke = False
                state = "randomSong2"
        elif state == "openSong": #play current song in 1 player mode
            if(musicPlayer.is_playing()):
                musicPlayer.quit_playing()
            musicPlayer.play("song.mp3")
            state = "randomSong"
        elif state == "openSong2": #play current song in 2 player mode
            if(musicPlayer.is_playing()):
                musicPlayer.quit_playing()
            musicPlayer.play("song.mp3")
            state = "randomSong2"
        elif state == "textToSpeech": #text to speech button
            if(textToSpeechEnabled == False):
                textToSpeechEnabled = True
                state = "settingsMenu"
            else:
                textToSpeechEnabled = False
                state = "settingsMenu"
                
        #soecify fps to 30 and update window
        clock.tick(30)
        pygame.display.update()
        
#method to get ablum cover from associated song after a guess        
def getAlbumnCover(songTitle):
    global curr_artist
    coverImage = album_cover_mappings.CoversByArtist(curr_artist, songTitle)
    imp = pygame.image.load(os.path.join('images', coverImage)).convert()
    gameDisplay.blit(imp, (500, 150))
        
#main menu screen
def mainMenu(events):
    title()
    button("Start 2 Player", 670, 360, 230, 50, color_dark, color_light, events, action="twoPlayer", mp3="startplayer2.mp3")
    button("Start 1 player", 400, 360, 230, 50, color_dark, color_light, events, action="onePlayer", mp3="startplayer1.mp3")
    button("Leaderboard", 400, 470, 230, 50, color_dark, color_light, events, action="leaderboard",mp3="leaderboard.mp3")
    button("Settings", 670, 470, 230, 50, color_dark, color_light, events, action="settingsMenu",mp3="settings.mp3")
    button("Quit", 0, 470, 130, 50, color_dark, color_light, events, action=end, mp3="quit.mp3")   
    
#render method, fills the screen with a color    
def render():
    gameDisplay.fill((4,107,153))

#handle when quit button is pressed
def end():
    if(musicPlayer.is_playing()):
        musicPlayer.quit_playing()
    pygame.quit()
    
#random song screen - 1 player
def randomSong(events, text, correct = None):
    global guessInstructionsSpoke
    gameDisplay.blit(text, ((0+(50/2)), (100+(50/2))))
    if(correct is not None):
         gameDisplay.blit(correct, ((0+(50/2)), (50+(50/2))))
    if(textToSpeechEnabled == True and not speechPlayer.is_playing() and guessInstructionsSpoke == False):
        speechPlayer.play(os.path.join('speechFiles', 'enterguessinstructions.mp3'))
        guessInstructionsSpoke = True
    button("Play current song", 340, 470, 290, 50, color_dark, color_light, events, action="openSong", mp3="opencurrentsong.mp3")
    button("Next song", 40, 470, 200, 50, color_dark, color_light, events, action="nextSong", mp3="nextsong.mp3")
    button("Quit", 900, 470, 130, 50, color_dark, color_light, events, action=end, mp3="quit.mp3")
    button("End Game", 670, 470, 200, 50, color_dark, color_light, events, action="endGame", mp3="mainMenu.mp3")
    if(onlyGuess == False):
        textinput.update(events)
        #Blit its surface onto the screen
        gameDisplay.blit(textinput.surface, (300, 300))
   
    
#random song screen - 2 player
def randomSong2(events, text, turnText, turnTalk, correct = None):
    global guessInstructionsSpoke
    global turnSpoke
    gameDisplay.blit(text, ((0+(50/2)), (100+(50/2))))
    if(correct is not None):
         gameDisplay.blit(correct, ((0+(50/2)), (50+(50/2))))
    gameDisplay.blit(turnText, ((0+(50/2)), (200+(50/2))) )
    if(textToSpeechEnabled == True):
        while(turnSpoke == False): 
            if(not speechPlayer.is_playing() and guessInstructionsSpoke == False):
                speechPlayer.play(os.path.join('speechFiles', 'enterguessinstructions.mp3'))
                guessInstructionsSpoke = True
            if(not speechPlayer.is_playing() and guessInstructionsSpoke == True):
                speechPlayer.play(os.path.join('speechFiles', turnTalk))
                turnSpoke = True
    button("Play current song", 340, 470, 290, 50, color_dark, color_light, events, action="openSong2", mp3="opencurrentsong.mp3")
    button("Next song", 40, 470, 200, 50, color_dark, color_light, events, action="nextSong2", mp3="nextsong.mp3")
    button("Quit", 900, 470, 130, 50, color_dark, color_light, events, action=end, mp3="quit.mp3")
    button("End Game", 670, 470, 200, 50, color_dark, color_light, events, action="endGame", mp3="mainMenu.mp3")
    if(onlyGuess == False):
        textinput.update(events)
       #Blit its surface onto the screen
        gameDisplay.blit(textinput.surface, (300, 300))

#one player select artist screen
def onePlayer(events):
    global curr_artist
    global textToSpeechEnabled
    global onePlayerInstructionsSpoke
    textOnePlay = smallfont.render("Select an artist for 1 player. Capitalization and punctuation are NOT needed.", True , white)
    gameDisplay.blit(textOnePlay, ((0+(50/2)), (100+(50/2))))
    if(textToSpeechEnabled == True and not speechPlayer.is_playing() and onePlayerInstructionsSpoke == False):
        speechPlayer.play(os.path.join('speechFiles', 'oneplayerinstructions.mp3'))
        onePlayerInstructionsSpoke = True

    #textinput.update(events)
    #gameDisplay.blit(textinput.surface, (300, 300))
    button("Nothing But Thieves", 150, 220, 230, 50, color_dark, color_light, events, "Nothing But Thieves", "randomSong", mp3="nothingbutthieves.mp3")
    button("Men I trust", 150, 280, 230, 50, color_dark, color_light, events, "Men I trust", "randomSong", mp3="menitrust.mp3")
    button("Arctic Monkeys", 150, 340, 230, 50, color_dark, color_light, events, "Arctic Monkeys", "randomSong", mp3="arcticmonkeys.mp3")
    button("Phish", 150, 400, 230, 50, color_dark, color_light, events, "Phish", "randomSong", mp3="phish.mp3")
    button("Billy Joel", 150, 460, 230, 50, color_dark, color_light, events, "Billy Joel", "randomSong", mp3="billyjoel.mp3")
    button("Cigarettes After Sex", 400, 220, 230, 50, color_dark, color_light, events, "Cigarettes After Sex", "randomSong", mp3="cigarettesaftersex.mp3")
    button("The Neighbourhood", 400, 280, 230, 50, color_dark, color_light, events, "The Neighbourhood", "randomSong", mp3="theneighbourhood.mp3")
    button("Five Finger Death Punch", 400, 340, 230, 50, color_dark, color_light, events, "Five Finger Death Punch", "randomSong",mp3="fivefingerdeathpunch.mp3")
    button("Coldplay", 400, 400, 230, 50, color_dark, color_light, events, "Coldplay", "randomSong",mp3="coldplay.mp3")
    button("Red Hot Chilli Peppers", 400, 460, 230, 50, color_dark, color_light, events, "Red Hot Chilli Peppers", "randomSong",mp3="redhotchillipeppers.mp3")
    button("Jimi Hendrix", 650, 220, 230, 50, color_dark, color_light, events, "Jimi Hendrix", "randomSong",mp3="jimihendrix.mp3")
    button("Glue Trip", 650, 280, 230, 50, color_dark, color_light, events, "Glue Trip", "randomSong",mp3="gluetrip.mp3")
    button("City and Colour", 650, 340, 230, 50, color_dark, color_light, events, "City and Colour", "randomSong",mp3="cityandcolour.mp3")
    button("Halestorm", 650, 400, 230, 50, color_dark, color_light, events, "Halestorm", "randomSong",mp3="halestorm.mp3")
    button("Diiv", 650, 460, 230, 50, color_dark, color_light, events, "Diiv", "randomSong",mp3="diiv.mp3")
    button("Green Day", 900, 220, 230, 50, color_dark, color_light, events, "Green Day", "randomSong",mp3="greenday.mp3")
    button("Crumb", 900, 280, 230, 50, color_dark, color_light, events, "Crumb", "randomSong",mp3="crumb.mp3")
    button("Peach Pit", 900, 340, 230, 50, color_dark, color_light, events, "Peach Pit", "randomSong",mp3="peachpit.mp3")
    button("The Fray", 900, 400, 230, 50, color_dark, color_light, events, "The Fray", "randomSong",mp3="thefray.mp3")
    button("Lil Nas X", 900, 460, 230, 50, color_dark, color_light, events, "Lil Nas X", "randomSong",mp3="lilnasx.mp3")
    # curr_artist = textinput.value
    button("Start", 450, 570, 130, 50, color_dark, color_light, events, action="randomSong",mp3="start.mp3")
    button("Back", 585, 570, 130, 50, color_dark, color_light, events, action="mainMenu",mp3="back.mp3")
    button("Quit", 720, 570, 130, 50, color_dark, color_light, events, action=end,mp3="quit.mp3")
   
#two player select artist screen
def twoPlayer(events):
   global curr_artist
   global twoPlayerInstructionsSpoke
   global turnSpoke
   textTwoPlay = smallfont.render("Select an artist for 2 players. Capitalization and punctuation are NOT needed.", True , white)
   startTurn = smallfont.render("Player 1's turn", True, white)
   gameDisplay.blit(textTwoPlay, ((0+(50/2)), (100+(50/2))))
   gameDisplay.blit(startTurn, ((0+(50/2)), (150+(50/2))))
#    textinput.update(events)
   gameDisplay.blit(textinput.surface, (300, 300))
#    curr_artist = textinput.value
   if(textToSpeechEnabled == True and not speechPlayer.is_playing() and twoPlayerInstructionsSpoke == False):
        speechPlayer.play(os.path.join('speechFiles', 'twoplayerinstructions.mp3'))
        twoPlayerInstructionsSpoke = True
   button("Nothing But Thieves", 150, 220, 230, 50, color_dark, color_light, events, "Nothing But Thieves", "randomSong2", mp3="nothingbutthieves.mp3")
   button("Men I trust", 150, 280, 230, 50, color_dark, color_light, events, "Men I trust", "randomSong2", mp3="menitrust.mp3")
   button("Arctic Monkeys", 150, 340, 230, 50, color_dark, color_light, events, "Arctic Monkeys", "randomSong2", mp3="arcticmonkeys.mp3")
   button("Phish", 150, 400, 230, 50, color_dark, color_light, events, "Phish", "randomSong2", mp3="phish.mp3")
   button("Billy Joel", 150, 460, 230, 50, color_dark, color_light, events, "Billy Joel", "randomSong2", mp3="billyjoel.mp3")
   button("Cigarettes After Sex", 400, 220, 230, 50, color_dark, color_light, events, "Cigarettes After Sex", "randomSong2", mp3="cigarettesaftersex.mp3")
   button("The Neighbourhood", 400, 280, 230, 50, color_dark, color_light, events, "The Neighbourhood", "randomSong2", mp3="theneighbourhood.mp3")
   button("Five Finger Death Punch", 400, 340, 230, 50, color_dark, color_light, events, "Five Finger Death Punch", "randomSong2",mp3="fivefingerdeathpunch.mp3")
   button("Coldplay", 400, 400, 230, 50, color_dark, color_light, events, "Coldplay", "randomSong2",mp3="coldplay.mp3")
   button("Red Hot Chilli Peppers", 400, 460, 230, 50, color_dark, color_light, events, "Red Hot Chilli Peppers", "randomSong2",mp3="redhotchillipeppers.mp3")
   button("Jimi Hendrix", 650, 220, 230, 50, color_dark, color_light, events, "Jimi Hendrix", "randomSong2",mp3="jimihendrix.mp3")
   button("Glue Trip", 650, 280, 230, 50, color_dark, color_light, events, "Glue Trip", "randomSong2",mp3="gluetrip.mp3")
   button("City and Colour", 650, 340, 230, 50, color_dark, color_light, events, "City and Colour", "randomSong2",mp3="cityandcolour.mp3")
   button("Halestorm", 650, 400, 230, 50, color_dark, color_light, events, "Halestorm", "randomSong2",mp3="halestorm.mp3")
   button("Diiv", 650, 460, 230, 50, color_dark, color_light, events, "Diiv", "randomSong2",mp3="diiv.mp3")
   button("Green Day", 900, 220, 230, 50, color_dark, color_light, events, "Green Day", "randomSong2",mp3="greenday.mp3")
   button("Crumb", 900, 280, 230, 50, color_dark, color_light, events, "Crumb", "randomSong2",mp3="crumb.mp3")
   button("Peach Pit", 900, 340, 230, 50, color_dark, color_light, events, "Peach Pit", "randomSong2",mp3="peachpit.mp3")
   button("The Fray", 900, 400, 230, 50, color_dark, color_light, events, "The Fray", "randomSong2",mp3="thefray.mp3")
   button("Lil Nas X", 900, 460, 230, 50, color_dark, color_light, events, "Lil Nas X", "randomSong2",mp3="lilnasx.mp3")
    # curr_artist = textinput.value
   button("Start", 450, 570, 130, 50, color_dark, color_light, events, action="randomSong",mp3="start.mp3")
   button("Back", 585, 570, 130, 50, color_dark, color_light, events, action="mainMenu",mp3="back.mp3")
   button("Quit", 720, 570, 130, 50, color_dark, color_light, events, action=end,mp3="quit.mp3")



#display title of game
def title():
    titleText = largefont.render("Guess That Song!" , True , white)
    gameDisplay.blit(titleText, ((370+(50/2)), (100+(50/2))))

#settings menu screen
def setting(events):
    global textToSpeechEnabled
    settingText = smallfont.render("Setting Menu", True, white)
    gameDisplay.blit(settingText, ((970+(50/2)), (100+(50/2))))
    button("Main Menu", 670, 470, 200, 50, color_dark, color_light, events, action="mainMenu",mp3="mainmenu.mp3")
    if(textToSpeechEnabled == False):
        button("Enable text to speech", 600, 370, 400, 50, color_dark, color_light, events, action="textToSpeech")
    else:
        button("Disable text to speech", 600, 370, 400, 50, color_dark, color_light, events, action="textToSpeech")
    button("Quit", 0, 470, 130, 50, color_dark, color_light, events, action=end,mp3="quit.mp3")

#game over screen
def gameOver(events):
    if(musicPlayer.is_playing()):
        musicPlayer.quit_playing()
    global leaderboardInformation
    global leaderboardNameEntered
    global onePlayerMode
    global gameOverSpoke
    global winnerSpoke
    gameOverText = smallfont.render("GAME OVER", True, white)
    gameDisplay.blit(gameOverText, ((500+(50/2)), (100+(50/2))))
    if(textToSpeechEnabled == True and not speechPlayer.is_playing() and gameOverSpoke == False):
        speechPlayer.play(os.path.join('speechFiles', 'gameover.mp3'))
        gameOverSpoke = True
    if(onePlayerMode):
        scorerText = smallfont.render("Score: " + str(score), True, white)
        gameDisplay.blit(scorerText, ((520+(50/2)), (150+(50/2))))
        leaderboardText = smallfont.render("Type your name and hit \"Enter\" to put your score in", True, white)
        gameDisplay.blit(leaderboardText, ((120+(50/2)), (200+(50/2))))
        leaderboardText2 = smallfont.render("the leaderboard (Maximum 8 characters)", True, white)
        gameDisplay.blit(leaderboardText2, ((120+(50/2)), (250+(50/2))))
        if(leaderboardNameEntered == False):
            textinput.update(events)
            gameDisplay.blit(textinput.surface, (300, 350))
            leaderboardInformation = False
        else:
            nameEntered = smallfont.render("Your name is now in the leaderboard", True, white)
            gameDisplay.blit(nameEntered, (300, 350))
    else:
        scorerText = smallfont.render("Player 1    -    Score: " + str(score) + "              Player 2    -    Score: " + str(scorePlayer2), True, white)
        if(score >= scorePlayer2):
            winnerText = smallfont.render("Player 1 Wins!", True, white)
            winnerTalk = "playeronewins.mp3"
        elif(score < scorePlayer2):
            winnerText = smallfont.render("Player 2 Wins!", True, white)
            winnerTalk = "playertwowins.mp3"
        gameDisplay.blit(scorerText, ((255+(50/2)), (150+(50/2))))
        gameDisplay.blit(winnerText, ((255+(50/2)), (250+(50/2))))
        if(textToSpeechEnabled == True and not speechPlayer.is_playing() and winnerSpoke == False):
            speechPlayer.play(os.path.join('speechFiles', winnerTalk))
            winnerSpoke = True
        

    button("Main Menu", 270, 470, 200, 50, color_dark, color_light, events, action="mainMenu", mp3="mainmenu.mp3")
    button("Quit", 670, 470, 130, 50, color_dark, color_light, events, action=end, mp3="quit.mp3")

#leaderboard screen
def leaderboard(events):
    global leaderboardInformation
    global infoDict
    if(leaderboardInformation==False):
        infoDict = lb.read_text()
        leaderboardInformation = True
    gameLeaderboardText = smallfont.render("Leaderboard - Top 20", True, white)
    gameDisplay.blit(gameLeaderboardText, ((450+(50/2)), (100+(50/2))))
    xAxis = 125
    yAxis = 175
    placement = 1
    for person in infoDict:
        personText = "#" + str(placement) + ": " + str(person) + " - Score: " + str(infoDict[person])
        gameLeadboardInfo = smallfont.render(personText, True, white)
        gameDisplay.blit(gameLeadboardInfo, (xAxis, yAxis))
        if(placement == 10):
            yAxis = 175
            xAxis = 725
        else:
            yAxis += 40
        placement += 1
    button("Main Menu", 270, 590, 200, 50, color_dark, color_light, events, action="mainMenu", mp3="mainmenu.mp3")
    button("Quit", 670, 590, 130, 50, color_dark, color_light, events, action=end, mp3="quit.mp3")

#method to update leaderboard with new entry
def updateLeaderboard():
    global infoDict
    infoDict = lb.read_text()
    newName = textinput.value[:8]
    infoDict[newName] = score
    infoDict = dict(sorted(infoDict.items(), key=lambda item: item[1], reverse=True))

    if len(infoDict) > 20:
        infoDict.popitem()

    lb.write_text(infoDict)


start()
