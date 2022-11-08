import pygame
import sys
import spotipy
import spotipy_artist
  
# initializing the constructor
pygame.init()
pygame.display.set_caption('Guess That Song')

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
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                loop = False
                end()
        render()
        print(state)
        if state == "mainMenu":
            mainMenu()
        elif state == "settingsMenu":
            setting()
        elif state == "onePlayer":
            onePlayer()
        elif state == "twoPlayer":
            twoPlayer()
        pygame.display.update()
        
        
        
def mainMenu():
    settingMenu = False
    render()
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

def onePlayer():
    result = spotipy_artist.get_artist("Michael Jackson")
    songDict = spotipy_artist.show_artist_top_tracks(result)
    textOnePlay = smallfont.render(songDict["Billie Jean"], True , white)
    gameDisplay.blit(textOnePlay, ((0+(50/2)), (100+(50/2))))
    button("Quit", 670, 470, 130, 50, color_dark, color_light, end)
    

def twoPlayer():
    textTwoPlay = smallfont.render("game started with 2 players" , True , white)
    gameDisplay.blit(textTwoPlay, ((0+(50/2)), (100+(50/2))))
    button("Quit", 670, 470, 130, 50, color_dark, color_light, end)

def title():
    titleText = largefont.render("Guess That Song!" , True , white)
    gameDisplay.blit(titleText, ((370+(50/2)), (100+(50/2))))

def setting():
    render()
    settingText = smallfont.render("Setting menu", True, white)
    gameDisplay.blit(settingText, ((970+(50/2)), (100+(50/2))))
    button("Main Menu", 670, 470, 130, 50, color_dark, color_light, "mainMenu")
    button("Quit", 0, 470, 130, 50, color_dark, color_light, end)

start()
