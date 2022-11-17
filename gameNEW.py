import pygame
import pygame_textinput
import sys
import spotipy
import spotipy_artist
import webbrowser
import random
  
"""
Artists that work with 10 songs:
1. Nothing But Thieves
2. Men I trust
3. Artic Monkeys
4. Phish
5. Michael Jackson
6. Cigarettes After Sex
7. The Neighbourhood
8. Five Finger Death Punch
9. Coldplay
10. Red Hot Chilli Peppers
11. Jimmy Hendrix
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

#make textbok
textinput = pygame_textinput.TextInputVisualizer()

running = True
settingMenu = False
state = "mainMenu"
  
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
songDict = {}
score = 0
scorePlayer2 = 0
turn = 1

#x - x coordinate of button
#y - y coordinate of button
#w - width of button
#h - height of button
#ic - unhighlighted color
#ac - highlighted color
#action - action (function) on button click
def button(msg,x,y,w,h,ic,ac,action=None):
    global state
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    if x+w > mouse[0] > x and y+h > mouse[1] > y:
        pygame.draw.rect(gameDisplay, ac,(x,y,w,h))
        
        if click[0] == 1 and action != None:
            if isinstance(action, str) == True:
                state = action
            else:
                action()
    else:
        pygame.draw.rect(gameDisplay, ic,(x,y,w,h))

    text = smallfont.render(msg , True , white)
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
            mainMenu()
        elif state == "settingsMenu":
            setting()
        elif state == "onePlayer":
            onePlayer(events)
        elif state == "twoPlayer":
             twoPlayer(events)
        elif state == "gameOver":
            gameOver()
        elif state == "randomSong":
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
                webbrowser.open(str(songLink))
                del songDict[songTitle]
                scoreFlag = False
                song_open = True
            if(len(songDict) == 0):
                song_open = False
                list_generated = False
                state = "gameOver"
            for event in events:
                if textinput.value.lower() == songTitle.lower() and event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                    if(not scoreFlag):
                        score += 1
                        scoreFlag = True
                    text = smallfont.render("Correct Guess!\nScore: " + str(score) , True , white)
                elif textinput.value.lower() != songTitle.lower() and event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                    text = smallfont.render("Incorrect Guess!\nScore: " + str(score) , True , white)
            randomSong(events, text)

        elif state == "randomSong2":
            if(not list_generated):
                result = spotipy_artist.get_artist(curr_artist)
                songDict = spotipy_artist.show_artist_top_tracks(result)
                list_generated = True
            if(not song_open and len(songDict) != 0):
                num_options = len(songDict) - 1
                randomNum = random.randint(0,num_options)
                songTitle = list(songDict)[randomNum]
                songLink = list(songDict.values())[randomNum]
                text = smallfont.render("Type the name of the song and click the \"Enter\" key.    Player 1 Score: " + str(score) + ", Player 2 score: " + str(scorePlayer2), True , white)
                webbrowser.open(str(songLink))
                del songDict[songTitle]
                scoreFlag = False
                song_open = True
            if(len(songDict) == 0):
                song_open = False
                list_generated = False
                state = "mainMenu"
            for event in events:
                if textinput.value.lower() == songTitle.lower() and event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                    if turn == 1:
                        if(not scoreFlag):
                            scoreFlag = True
                            score += 1
                            turn = 2
                    elif turn == 2:
                        if(not scoreFlag):
                            scoreFlag = True
                            scorePlayer2 +=1
                            turn = 1
                    text = smallfont.render("Correct Guess!\nPlayer 1 Score: " + str(score) + ", Player 2 score: " + str(scorePlayer2), True , white)
                elif textinput.value.lower() != songTitle.lower() and event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                    text = smallfont.render("Incorrect Guess!\nPlayer 1 Score: " + str(score) + ", Player 2 score: " + str(scorePlayer2), True , white)
                    if turn == 1:
                        turn = 2
                    elif turn == 2:
                        turn = 1
            randomSong2(events, text)
        elif state == "nextSong":
            song_open = False
            state = "randomSong"
        elif state == "nextSong2":
            song_open = False
            state = "randomSong2"
        clock.tick(30)
        pygame.display.update()
        
        
        
def mainMenu():
    settingMenu = False
    title()
    button("Start 2 Player", 670, 360, 230, 50, color_dark, color_light, "twoPlayer")
    button("Start 1 player", 400, 360, 230, 50, color_dark, color_light, "onePlayer")
    button("Settings", 400, 470, 130, 50, color_dark, color_light, "settingsMenu")
    button("Quit", 0, 470, 130, 50, color_dark, color_light, end)
              
    #make switch case that checks current state, then calls each state's respective function. should be alot cleaner code
    
def render():
    # fills the screen with a color
    gameDisplay.fill((4,215,250))

def end():
    pygame.quit()
    

def randomSong(events, text):
    gameDisplay.blit(text, ((0+(50/2)), (100+(50/2))))
    button("Next song", 40, 470, 130, 50, color_dark, color_light, "nextSong")
    button("Quit", 670, 470, 130, 50, color_dark, color_light, end)
    textinput.update(events)
    # Blit its surface onto the screen
    gameDisplay.blit(textinput.surface, (300, 300))
    

def randomSong2(events, text):
    gameDisplay.blit(text, ((0+(50/2)), (100+(50/2))))
    button("Next song", 40, 470, 130, 50, color_dark, color_light, "nextSong2")
    button("Quit", 670, 470, 130, 50, color_dark, color_light, end)
    textinput.update(events)
    # Blit its surface onto the screen
    gameDisplay.blit(textinput.surface, (300, 300))

def onePlayer(events):
    global curr_artist
    textOnePlay = smallfont.render("Enter an artist for 1 player. Punctuation is needed but capitalization is not.", True , white)
    gameDisplay.blit(textOnePlay, ((0+(50/2)), (100+(50/2))))
    textinput.update(events)
    gameDisplay.blit(textinput.surface, (300, 300))
    curr_artist = textinput.value
    button("Random Song", 270, 470, 290, 50, color_dark, color_light, "randomSong")
    button("Quit", 670, 470, 130, 50, color_dark, color_light, end)
    
        

def twoPlayer(events):
   global curr_artist
   textTwoPlay = smallfont.render("Enter an artist for 2 players. Punctuation is needed but capitalization is not.", True , white)
   gameDisplay.blit(textTwoPlay, ((0+(50/2)), (100+(50/2))))
   textinput.update(events)
   gameDisplay.blit(textinput.surface, (300, 300))
   curr_artist = textinput.value
   button("Random Song", 270, 470, 290, 50, color_dark, color_light, "randomSong2")
   button("Quit", 670, 470, 130, 50, color_dark, color_light, end)

def title():
    titleText = largefont.render("Guess That Song!" , True , white)
    gameDisplay.blit(titleText, ((370+(50/2)), (100+(50/2))))

def setting():
    settingText = smallfont.render("Setting menu", True, white)
    gameDisplay.blit(settingText, ((970+(50/2)), (100+(50/2))))
    button("Main Menu", 670, 470, 130, 50, color_dark, color_light, "mainMenu")
    button("Quit", 0, 470, 130, 50, color_dark, color_light, end)

def gameOver():
    gameOverText = smallfont.render("GAME OVER", True, white)
    gameDisplay.blit(gameOverText, ((970+(50/2)), (100+(50/2))))
    scorerText = smallfont.render("Score: " + str(score), True, white)
    gameDisplay.blit(scorerText, ((500+(50/2)), (300+(50/2))))
    button("Main Menu", 270, 470, 130, 50, color_dark, color_light, "mainMenu")
    button("Quit", 670, 470, 130, 50, color_dark, color_light, end)

start()
