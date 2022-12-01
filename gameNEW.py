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
import time
import subprocess
from threading import Thread

# https://stackoverflow.com/questions/21629727/how-to-delay-pygame-key-get-pressed
  
"""
Artists that work with 10 songs:
1. Nothing But Thieves
2. Men I trust
3. Arctic Monkeys
4. Phish
5. Billy Joel
6. Cigarettes After Sex
7. The Neighbourhood
8. Five Finger Death Punch
9. Coldplay
10. Red Hot Chilli Peppers
11. Jimi Hendrix
12. Glue Trip
13. City and Colour
14. Halestorm
15. Diiv
16. Green Day
17. Crumb
18. Peach Pit
19. The Fray
20. Lil Nas X
"""


# initializing the constructor
pygame.init()
clock = pygame.time.Clock()
pygame.display.set_caption('Guess That Song')
pygame.key.set_repeat(500, 50) # allow user to hold down key and detect it

#make textbox
textinput = pygame_textinput.TextInputVisualizer()
textinput.font_color = (255, 255, 255)
textinput.cursor_color = (255, 255, 255)

running = True
settingMenu = False
state = "mainMenu"
firstGuess = True
  
# screen resolution
res = (1280,720)
  
# opens up a window
gameDisplay = pygame.display.set_mode(res)
  
# white color
white = (255,255,255)
  
# light shade of the button
color_light = (170,170,170)
  
# dark shade of the button
color_dark = (100,100,100)
  
# stores the width of the
# screen into a variable
width = gameDisplay.get_width()
  
# stores the height of the
# screen into a variable
height = gameDisplay.get_height()
  
# defining a font
smallerfont = pygame.font.SysFont('Corbel',18)
smallfont = pygame.font.SysFont('Corbel',35)
largefont = pygame.font.SysFont('Corbel',80)
  
# rendering a text written in
# this font

#flag for only opening tab once
song_open = False

#flag to see if list is generated
list_generated = False

#information used during the gameplay
curr_artist = ""
songLink = ""
songDict = {}
score = 0
scorePlayer2 = 0
turn = 1
leaderboardInformation = False
infoDict = dict()
leaderboardNameEntered = False
onePlayerMode = True
textToSpeechEnabled = False

onlyGuess = False
#-------------------------------------------------------------------
# MusicPlayer class
#-------------------------------------------------------------------
class MusicPlayer():
    """
    Start a subprocess running audio player mpg123 to play a specified
    mp3 file. Provide controls to stop/start and quit playback.
    """
    def __init__(self):
        self._audioengine = 'mpg123' # Only supported player is mpg123
        self._p = None
        self._is_paused = False

        # The following instance variables are affected by the process_monitor
        # thread. 
        self._process_running = False
        self._return_code = None


    def play(self, sound_file):
        if not self._process_running:
            try:
                # Open a subprocess that runs mpg123 to play an mp3 file
                self._p = subprocess.Popen([self._audioengine, 
                                      '-C',     # Enable commands to be read from stdin
                                      '-q',     # Be quiet
                                      sound_file],
                                      stdin=subprocess.PIPE, # Pipe input via bytes
                                      stdout=None,   
                                      stderr=None)

                # Since we are using stdin for commands, we have to send something
                # to keep mpg123 from complaining when we exit. The complaint is
                # not a serious one, but it is annoying. If stdin is not used the
                # terminal is posted with "Can't set terminal attributes" at exit.
                # I send an empty string below to keep mpg123 happy.
                self._p.stdin.write(b'')
                self._p.stdin.flush()

                # start a monitor thread that sets instance variables with the
                # status of the subprocess. 
                monitor_thread = Thread(target=self.process_monitor,args=()) 
                monitor_thread.start()

            except FileNotFoundError as e:
                raise AudioEngineUnavailableError(f'AudioEngineUnavailableError: {e}')
        else:
            raise PlaybackInProgressError('You cannot play while something else is already playing.')

    def quit_playing(self):
        if self._process_running:
            self._p.stdin.write(b'q')
            self._p.stdin.flush()

            # Wait for process to end
            while self._process_running:
                time.sleep(0.1)
        else:
            raise NoPlaybackError('Cannot quit playback because nothing is playing.')

    def pause(self):
        if self._process_running:
            if self._is_paused:
                # Already paused, do nothing
                pass
            else:
                self._p.stdin.write(b's')
                self._p.stdin.flush()
                self._is_paused = True
        else:
            raise NoPlaybackError('Cannot pause playback because nothing is playing.')
                    
    def resume(self):
        if self._process_running:
            if not self._is_paused:
                # Already playing, do nothing
                pass
            else:
                self._p.stdin.write(b's')
                self._p.stdin.flush()
                self._is_paused = False
        else:
            raise NoPlaybackError('Cannot resume playback because nothing is playing.')

    def is_playing(self):
        return self._process_running

    def return_code(self):
        return self._return_code

    def process_monitor(self):
        """
        This code runs in its own thread to monitor the state of our
        external subprocess. Instance variables _process_running and
        _return_code are used to show the process status.
        """
        # Indicate that the process is running at the start, it
        # should be
        self._process_running = True

        # When a process exits, p.poll() returns the code it set upon
        # completion
        self._return_code = self._p.poll()

        # See whether the process has already exited. This will cause a
        # value (i.e. not None) to return from p.poll()
        if self._return_code == None:
            # Wait for the process to complete, get its return code directly
            # from the wait() call (i.e. do not use p.poll())
            self._return_code = self._p.wait()

        # When we get here, the process has exited and set a return code
        self._process_running = False
player = MusicPlayer()

#x - x coordinate of button
#y - y coordinate of button
#w - width of button
#h - height of button
#ic - unhighlighted color
#ac - highlighted color
#action - action (function) on button click
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
    if x+w > mouse[0] > x and y+h > mouse[1] > y:
        pygame.draw.rect(gameDisplay, ac,(x,y,w,h))
        if(textToSpeechEnabled == True and action != "textToSpeech" and not player.is_playing()):
            player.play(mp3)
        if clicked and action != None:
            if artist != None:
                curr_artist = artist
            if isinstance(action, str) == True:
                state = action
            else:
                action()
    else:
        pygame.draw.rect(gameDisplay, ic,(x,y,w,h))
    if artist == None:
        text = smallfont.render(msg , True , white)
    else:
        text = smallerfont.render(msg , True , white)
    gameDisplay.blit(text, ( (x+(w/5.5)), (y+(h/3)) ))

def start():
    loop()
    end()
    
def loop():
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
    scoreFlag = False
    running = True
    result = ""
    songDict = ""
    text = ""
    while running:
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                loop = False
                end()
        render()
        
        if state == "mainMenu":
            mainMenu(events)
        elif state == "settingsMenu":
            setting(events)
        elif state == "leaderboard":
            leaderboard(events)
        elif state == "onePlayer":
            score = 0
            leaderboardNameEntered = False
            onePlayerMode = True
            onePlayer(events)
        elif state == "twoPlayer":
            score = 0
            scorePlayer2 = 0
            turn = 1
            leaderboardNameEntered = False
            onePlayerMode = False
            twoPlayer(events)
        elif state == "gameOver":
            gameOver(events)
            firstGuess = True
            for event in events:
                if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN and leaderboardNameEntered == False:
                    updateLeaderboard()
                    leaderboardNameEntered = True
        elif state == "randomSong":
            if(firstGuess):
                firstGuess = False
                textinput.value = ""
            if(not list_generated):
                result = spotipy_artist.get_artist(curr_artist)
                songDict = spotipy_artist.show_artist_top_tracks(result)
                # print(songDict)
                list_generated = True
            if(not song_open and len(songDict) != 0):
                num_options = len(songDict) - 1
                randomNum = random.randint(0,num_options)
                songTitle = list(songDict)[randomNum]
                songLink = list(songDict.values())[randomNum]
                text = smallfont.render("Type the name of the song and click the \"Enter\" key.    Score: " + str(score), True , white)
                # print(songTitle)
                # print(songLink)
                webbrowser.open(str(songLink))
                del songDict[songTitle]
                scoreFlag = False
                song_open = True
            
            for event in events:
                if re.sub('[^A-Za-z0-9]+', '', textinput.value.lower()) == re.sub('[^A-Za-z0-9]+', '', songTitle.lower()) and event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                    onlyGuess = True
                    if(not scoreFlag):
                        score += 1
                        scoreFlag = True
                    text = smallfont.render("Correct Guess!    Score: " + str(score) , True , white)
                elif textinput.value.lower() != songTitle.lower() and event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                    onlyGuess = True
                    text = smallfont.render("Incorrect Guess!    Score: " + str(score) , True , white)
            randomSong(events, text)

        elif state == "randomSong2":
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
                elif turn == 2:
                    turnText = player2Turn
                webbrowser.open(str(songLink))
                del songDict[songTitle]
                scoreFlag = False
                song_open = True
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
                elif textinput.value.lower() != songTitle.lower() and event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                    onlyGuess = True
                    text = smallfont.render("Incorrect Guess!    Player 1 Score: " + str(score) + ", Player 2 Score: " + str(scorePlayer2), True , white)
                    if turn == 1:
                        turn = 2
                    elif turn == 2:
                        turn = 1
            randomSong2(events, text, turnText)
        elif state == "nextSong":
            textinput.value = ""
            clock.tick(30)
            song_open = False
            pygame.mouse.set_pos(150, 419)
            if(len(songDict) == 0):
                list_generated = False
                state = "gameOver"
            else:
                onlyGuess = False
                state = "randomSong"
        elif state == "nextSong2":
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
                state = "randomSong2"
        elif state == "openSong":
            webbrowser.open(str(songLink))
            state = "randomSong"
        elif state == "openSong2":
            webbrowser.open(str(songLink))
            state = "randomSong2"
        elif state == "textToSpeech":
            if(textToSpeechEnabled == False):
                textToSpeechEnabled = True
                state = "settingsMenu"
            else:
                textToSpeechEnabled = False
                state = "settingsMenu"
        clock.tick(30)
        pygame.display.update()
        
        
        
def mainMenu(events):
    settingMenu = False
    title()
    button("Start 2 Player", 670, 360, 230, 50, color_dark, color_light, events, action="twoPlayer", mp3="startplayer2.mp3")
    button("Start 1 player", 400, 360, 230, 50, color_dark, color_light, events, action="onePlayer", mp3="startplayer1.mp3")
    button("Leaderboard", 400, 470, 230, 50, color_dark, color_light, events, action="leaderboard",mp3="leaderboard.mp3")
    button("Settings", 670, 470, 230, 50, color_dark, color_light, events, action="settingsMenu",mp3="settings.mp3")
    button("Quit", 0, 470, 130, 50, color_dark, color_light, events, action=end, mp3="quit.mp3")
              
    #make switch case that checks current state, then calls each state's respective function. should be alot cleaner code
    
def render():
    # fills the screen with a color
    gameDisplay.fill((4,107,153))

def end():
    pygame.quit()
    

def randomSong(events, text):
    gameDisplay.blit(text, ((0+(50/2)), (100+(50/2))))
    button("Open current song", 340, 470, 290, 50, color_dark, color_light, events, action="openSong", mp3="opencurrentsong.mp3")
    button("Next song", 40, 470, 200, 50, color_dark, color_light, events, action="nextSong", mp3="nextsong.mp3")
    button("Quit", 670, 470, 130, 50, color_dark, color_light, events, action=end, mp3="quit.mp3")
    if(onlyGuess == False):
        textinput.update(events)
    # Blit its surface onto the screen
        gameDisplay.blit(textinput.surface, (300, 300))
    

def randomSong2(events, text, turnText):
    gameDisplay.blit(text, ((0+(50/2)), (100+(50/2))))
    gameDisplay.blit(turnText, ((0+(50/2)), (200+(50/2))) )
    button("Open current song", 340, 470, 290, 50, color_dark, color_light, events, action="openSong2", mp3="opencurrentsong.mp3")
    button("Next song", 40, 470, 200, 50, color_dark, color_light, events, action="nextSong2", mp3="nextsong.mp3")
    button("Quit", 670, 470, 130, 50, color_dark, color_light, events, action=end, mp3="quit.mp3")
    if(onlyGuess == False):
        textinput.update(events)
    # Blit its surface onto the screen
        gameDisplay.blit(textinput.surface, (300, 300))

def onePlayer(events):
    global curr_artist
    textOnePlay = smallfont.render("Select an artist for 1 player. Capitalization and punctuation are NOT needed.", True , white)
    gameDisplay.blit(textOnePlay, ((0+(50/2)), (100+(50/2))))
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

def twoPlayer(events):
   global curr_artist
   textTwoPlay = smallfont.render("Select an artist for 2 players. Capitalization and punctuation are NOT needed.", True , white)
   startTurn = smallfont.render("Player 1's turn", True, white)
   gameDisplay.blit(textTwoPlay, ((0+(50/2)), (100+(50/2))))
   gameDisplay.blit(startTurn, ((0+(50/2)), (150+(50/2))))
#    textinput.update(events)
   gameDisplay.blit(textinput.surface, (300, 300))
#    curr_artist = textinput.value
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

def title():
    titleText = largefont.render("Guess That Song!" , True , white)
    gameDisplay.blit(titleText, ((370+(50/2)), (100+(50/2))))

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

def gameOver(events):
    global leaderboardInformation
    global leaderboardNameEntered
    global onePlayerMode
    gameOverText = smallfont.render("GAME OVER", True, white)
    gameDisplay.blit(gameOverText, ((500+(50/2)), (100+(50/2))))
    
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
        gameDisplay.blit(scorerText, ((255+(50/2)), (150+(50/2))))
        

    button("Main Menu", 270, 470, 200, 50, color_dark, color_light, events, action="mainMenu", mp3="mainmenu.mp3")
    button("Quit", 670, 470, 130, 50, color_dark, color_light, events, action=end, mp3="quit.mp3")

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
