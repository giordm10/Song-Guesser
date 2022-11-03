import pygame
import sys
import spotipy
  
# initializing the constructor
pygame.init()


running = True
  
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
  
# rendering a text written in
# this font


def button(msg,x,y,w,h,ic,ac,action=None):
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    print(click)
    if x+w > mouse[0] > x and y+h > mouse[1] > y:
        pygame.draw.rect(gameDisplay, ac,(x,y,w,h))
        
        if click[0] == 1 and action != None:
            action()
    else:
        pygame.draw.rect(gameDisplay, ic,(x,y,w,h))

    text = smallfont.render(msg , True , white)
    gameDisplay.blit(text, ( (x+(w/2)), (y+(h/2)) ))

def start():
    loop()
    cleanUp()

def loop():
    global running
    while running:
	      
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        button("Quit", 360, 360, 100, 100, color_dark, color_light, cleanUp);
              
        # updates the frames of the game
        pygame.display.update()
    
def render():
    # fills the screen with a color
    gameDisplay.fill((0,0,0))

def cleanUp():
    print("cleaning up")
    pygame.quit()

start()
