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
    mouse = pygame.mouse.get_pos()
    if x+w > mouse[0] > x and y+h > mouse[1] > y:
        pygame.draw.rect(gameDisplay, ac,(x,y,w,h))
        if(textToSpeechEnabled == True):
            os.system("mpg123 " + mp3)
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
    button("Quit", 0, 470, 130, 50, color_dark, color_light, events, action=end)
              
    #make switch case that checks current state, then calls each state's respective function. should be alot cleaner code
    
def render():
    # fills the screen with a color
    gameDisplay.fill((4,107,153))

def end():
    pygame.quit()
    

def randomSong(events, text):
    gameDisplay.blit(text, ((0+(50/2)), (100+(50/2))))
<<<<<<< HEAD
    button("Next song", 40, 470, 200, 50, color_dark, color_light, events, action="nextSong", mp3="nextsong.mp3")
=======
    button("Open current song", 340, 470, 290, 50, color_dark, color_light, events, action="openSong")
    button("Next song", 40, 470, 200, 50, color_dark, color_light, events, action="nextSong")
>>>>>>> f7b2e56ff909e92bba4e8bea6367e1d1e8f5c580
    button("Quit", 670, 470, 130, 50, color_dark, color_light, events, action=end)
    if(onlyGuess == False):
        textinput.update(events)
    # Blit its surface onto the screen
        gameDisplay.blit(textinput.surface, (300, 300))
    

def randomSong2(events, text, turnText):
    gameDisplay.blit(text, ((0+(50/2)), (100+(50/2))))
    gameDisplay.blit(turnText, ((0+(50/2)), (200+(50/2))) )
    button("Open current song", 340, 470, 290, 50, color_dark, color_light, events, action="openSong2")
    button("Next song", 40, 470, 200, 50, color_dark, color_light, events, action="nextSong2")
    button("Quit", 670, 470, 130, 50, color_dark, color_light, events, action=end)
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
    button("Nothing But Thieves", 150, 220, 230, 50, color_dark, color_light, events, "Nothing But Thieves", "randomSong")
    button("Men I trust", 150, 280, 230, 50, color_dark, color_light, events, "Men I trust", "randomSong")
    button("Arctic Monkeys", 150, 340, 230, 50, color_dark, color_light, events, "Arctic Monkeys", "randomSong")
    button("Phish", 150, 400, 230, 50, color_dark, color_light, events, "Phish", "randomSong")
    button("Billy Joel", 150, 460, 230, 50, color_dark, color_light, events, "Billy Joel", "randomSong")
    button("Cigarettes After Sex", 400, 220, 230, 50, color_dark, color_light, events, "Cigarettes After Sex", "randomSong")
    button("The Neighbourhood", 400, 280, 230, 50, color_dark, color_light, events, "The Neighbourhood", "randomSong")
    button("Five Finger Death Punch", 400, 340, 230, 50, color_dark, color_light, events, "Five Finger Death Punch", "randomSong")
    button("Coldplay", 400, 400, 230, 50, color_dark, color_light, events, "Coldplay", "randomSong")
    button("Red Hot Chilli Peppers", 400, 460, 230, 50, color_dark, color_light, events, "Red Hot Chilli Peppers", "randomSong")
    button("Jimi Hendrix", 650, 220, 230, 50, color_dark, color_light, events, "Jimi Hendrix", "randomSong")
    button("Glue Trip", 650, 280, 230, 50, color_dark, color_light, events, "Glue Trip", "randomSong")
    button("City and Colour", 650, 340, 230, 50, color_dark, color_light, events, "City and Colour", "randomSong")
    button("Halestorm", 650, 400, 230, 50, color_dark, color_light, events, "Halestorm", "randomSong")
    button("Diiv", 650, 460, 230, 50, color_dark, color_light, events, "Diiv", "randomSong")
    button("Green Day", 900, 220, 230, 50, color_dark, color_light, events, "Green Day", "randomSong")
    button("Crumb", 900, 280, 230, 50, color_dark, color_light, events, "Crumb", "randomSong")
    button("Peach Pit", 900, 340, 230, 50, color_dark, color_light, events, "Peach Pit", "randomSong")
    button("The Fray", 900, 400, 230, 50, color_dark, color_light, events, "The Fray", "randomSong")
    button("Lil Nas X", 900, 460, 230, 50, color_dark, color_light, events, "Lil Nas X", "randomSong")
    # curr_artist = textinput.value
    button("Start", 450, 570, 130, 50, color_dark, color_light, events, action="randomSong")
    button("Back", 585, 570, 130, 50, color_dark, color_light, events, action="mainMenu")
    button("Quit", 720, 570, 130, 50, color_dark, color_light, events, action=end)

def twoPlayer(events):
   global curr_artist
   textTwoPlay = smallfont.render("Select an artist for 2 players. Capitalization and punctuation are NOT needed.", True , white)
   startTurn = smallfont.render("Player 1's turn", True, white)
   gameDisplay.blit(textTwoPlay, ((0+(50/2)), (100+(50/2))))
   gameDisplay.blit(startTurn, ((0+(50/2)), (150+(50/2))))
#    textinput.update(events)
   gameDisplay.blit(textinput.surface, (300, 300))
#    curr_artist = textinput.value
   button("Nothing But Thieves", 150, 220, 230, 50, color_dark, color_light, events, "Nothing But Thieves", "randomSong2")
   button("Men I trust", 150, 280, 230, 50, color_dark, color_light, events, "Men I trust", "randomSong2")
   button("Arctic Monkeys", 150, 340, 230, 50, color_dark, color_light, events, "Arctic Monkeys", "randomSong2")
   button("Phish", 150, 400, 230, 50, color_dark, color_light, events, "Phish", "randomSong2")
   button("Billy Joel", 150, 460, 230, 50, color_dark, color_light, events, "Billy Joel", "randomSong2")
   button("Cigarettes After Sex", 400, 220, 230, 50, color_dark, color_light, events, "Cigarettes After Sex", "randomSong2")
   button("The Neighbourhood", 400, 280, 230, 50, color_dark, color_light, events, "The Neighbourhood", "randomSong2")
   button("Five Finger Death Punch", 400, 340, 230, 50, color_dark, color_light, events, "Five Finger Death Punch", "randomSong2")
   button("Coldplay", 400, 400, 230, 50, color_dark, color_light, events, "Coldplay", "randomSong2")
   button("Red Hot Chilli Peppers", 400, 460, 230, 50, color_dark, color_light, events, "Red Hot Chilli Peppers", "randomSong2")
   button("Jimi Hendrix", 650, 220, 230, 50, color_dark, color_light, events, "Jimi Hendrix", "randomSong2")
   button("Glue Trip", 650, 280, 230, 50, color_dark, color_light, events, "Glue Trip", "randomSong2")
   button("City and Colour", 650, 340, 230, 50, color_dark, color_light, events, "City and Colour", "randomSong2")
   button("Halestorm", 650, 400, 230, 50, color_dark, color_light, events, "Halestorm", "randomSong2")
   button("Diiv", 650, 460, 230, 50, color_dark, color_light, events, "Diiv", "randomSong2")
   button("Green Day", 900, 220, 230, 50, color_dark, color_light, events, "Green Day", "randomSong2")
   button("Crumb", 900, 280, 230, 50, color_dark, color_light, events, "Crumb", "randomSong2")
   button("Peach Pit", 900, 340, 230, 50, color_dark, color_light, events, "Peach Pit", "randomSong2")
   button("The Fray", 900, 400, 230, 50, color_dark, color_light, events, "The Fray", "randomSong2")
   button("Lil Nas X", 900, 460, 230, 50, color_dark, color_light, events, "Lil Nas X", "randomSong2")
   button("Start", 450, 570, 130, 50, color_dark, color_light, events, action="randomSong")
   button("Back", 585, 570, 130, 50, color_dark, color_light, events, action="mainMenu")
   button("Quit", 720, 570, 130, 50, color_dark, color_light, events, action=end)

def title():
    titleText = largefont.render("Guess That Song!" , True , white)
    gameDisplay.blit(titleText, ((370+(50/2)), (100+(50/2))))

def setting(events):
    global textToSpeechEnabled
    settingText = smallfont.render("Setting Menu", True, white)
    gameDisplay.blit(settingText, ((970+(50/2)), (100+(50/2))))
    button("Main Menu", 670, 470, 200, 50, color_dark, color_light, events, action="mainMenu")
    if(textToSpeechEnabled == False):
        button("Enable text to speech", 600, 370, 400, 50, color_dark, color_light, events, action="textToSpeech")
    else:
        button("Disable text to speech", 600, 370, 400, 50, color_dark, color_light, events, action="textToSpeech")
    button("Quit", 0, 470, 130, 50, color_dark, color_light, events, action=end)

def gameOver(events):
    global leaderboardInformation
    global leaderboardNameEntered
    global onePlayerMode
    gameOverText = smallfont.render("GAME OVER", True, white)
    gameDisplay.blit(gameOverText, ((500+(50/2)), (100+(50/2))))
    scorerText = smallfont.render("Score: " + str(score), True, white)
    gameDisplay.blit(scorerText, ((520+(50/2)), (150+(50/2))))
    if(onePlayerMode):
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

    button("Main Menu", 270, 470, 200, 50, color_dark, color_light, events, action="mainMenu")
    button("Quit", 670, 470, 130, 50, color_dark, color_light, events, action=end)

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
    button("Main Menu", 270, 590, 200, 50, color_dark, color_light, events, action="mainMenu")
    button("Quit", 670, 590, 130, 50, color_dark, color_light, events, action=end)

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