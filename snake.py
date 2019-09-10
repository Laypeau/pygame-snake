# Amazing snake game
# Adapted from project by Samuel Backman by Nathan Duong
# Original can be found at https://www.pygame.org/project/818/1409

import pygame, random, sys
from pygame.locals import *
highscore = open("highscore.txt").read()

            #DEFINING FUNCTIONS
#Defines the collision function
def collide(x1, x2, y1, y2, w1, w2, h1, h2):
    if x1+w1>x2 and x1<x2+w2 and y1+h1>y2 and y1<y2+h2:
        return True
    else:
        return False

#Define the death function
def die(screen, score):
    font = pygame.font.SysFont("Arial", 20, (255,255,255)); #Defines font again, but bigger
    gameend_text = font.render("Your score was: " + str(score), True, (255, 255, 255)) #Creates death text. font.render(string, antialiasing, colour)
    highscore_text = font.render("You beat the highscore of " + str(highscore) +"!", True, (255, 255, 255));
    screen.blit(gameend_text, (10, 270)); #Actually draws the text
    if score > int(highscore):
        name = open("highscore.txt", "w")
        name.write(str(score))
        name.close()
        screen.blit(highscore_text, (10, 290))
    pygame.display.update(); #Updates the display with the text on it (So the text appears)
    pygame.time.wait(2500); #Waits 25 seconds
    sys.exit(0) #Exit game

            #SETTING VARIABLES
#Sets the positions for the first five segments in the snake
#Each segment of the snake has it's x and y co-ordinates stored in these two lists
segment_x = [50, 30, 30, 30, 30] 
segment_y = [230, 230, 230, 230, 230]

direction = "east" #Direction variable for the snake head
score = 0 #Increments by one each time an apple is eaten
highscore = open("highscore.txt").read()

appleseq_x = [30, 50, 70, 90, 110, 130, 150, 170, 190, 210, 230, 250, 270, 290, 310, 330] #Because random.randint() is dumb
appleseq_y = [70, 90, 110, 130, 150, 170, 190, 210, 230, 250, 270, 290, 310, 330, 350, 370]
applepos = ((random.choice(appleseq_x), random.choice(appleseq_y))) #Sets apple position. Don't spawn on snake!

#Initialise Pygame
pygame.init(); #initialises pygame wow
screen = pygame.display.set_mode((380, 420)); #Window resolution
pygame.display.set_caption("Snake"); #Window title
font = pygame.font.SysFont("Arial", 25, True); #Sets f to a font to display the score
clock = pygame.time.Clock() #Creates a clock

#define the apple as a pygame surface
appleimage = pygame.Surface((20, 20)); #pygame.Surface() creates a sprite, taking in dimension parameters to draw a blank one
appleimage.fill((0, 255, 0)); #Fills the surface with a flat colour

#Define a snake segment as a pygame surface
img = pygame.Surface((20,20));
img.fill((255, 0, 0));

#Define the background image as a surface
bgimage = pygame.image.load("aaa.png").convert()

            #MAIN LOOP
while True:
    clock.tick(10)

    #Checks the event stack
    for e in pygame.event.get():
        if e.type == QUIT:
            sys.exit(0)
            
        #This is the part I drew the algorithm on. It handles keyboard controls
        elif e.type == KEYDOWN:
            if e.key == K_UP and direction != "south":
                direction = "north"
                print("keydown north")
                break
            elif e.key == K_DOWN and direction != "north":
                direction = "south"
                print("keydown south")
                break
            elif e.key == K_LEFT and direction != "east":
                direction = "west"
                print("keydown west")
                break
            elif e.key == K_RIGHT and direction != "west":
                direction = "east"
                print("keydown east")
                break

    print("Final keydown: " + direction)
    
    #Checks a collision with self
    i = len(segment_x)-1
    while i >= 2:
        if collide(segment_x[0], segment_x[i], segment_y[0], segment_y[i], 20, 20, 20, 20):
            print("death: collision with self")
            die(screen, score)
        i-= 1

    #Checks and handles a collision with the apple
    if collide(segment_x[0], applepos[0], segment_y[0], applepos[1], 20, 10, 20, 10):
        print("event: apple collected")
        score+=1;
        segment_x.append(700) #Appends a segment off-screen, which is teleported to the end of the snake when it moves, before the frame is rendered.
        segment_y.append(700) #I can't add more than one segment per frame without some effort
        applepos = ((random.choice(appleseq_x),  random.choice(appleseq_y)))
        while applepos[0] in segment_x:
            applepos = ((random.choice(appleseq_x), applepos[1]))
            print("apple x changed")
        while applepos[1] in segment_y:
            print("apple y changed")
            applepos = (applepos[0],  random.choice(appleseq_y)) 
        print("Event: apple relocation to " +  str(applepos))

    #If outside of play area      
    if segment_x[0] < 30 or segment_x[0] >= 350 or segment_y[0] < 70 or segment_y[0] >= 390:
        
        print("death: out of bounds at ", str(segment_x[0]) + ", " + str(segment_y[0]) )
        die(screen, score)
    
    #This part moves the snake. It was in a while loop for some reason before, which was bad
    #For each segment of the snake that isn't the first, set it's position to the one before it in the list
    for i in range(len(segment_x)-1, 0, -1):
        segment_x[i] = segment_x[i-1]
        segment_y[i] = segment_y[i-1]
        
    #For the snake head, move it 20 units in the direction of movement
    if direction=="south":
        segment_y[0] += 20
    elif direction=="east":
        segment_x[0] += 20
    elif direction=="north":
        segment_y[0] -= 20
    elif direction=="west":
        segment_x[0] -= 20

    #RENDER TIME
    #Creates the background
    screen.blit(bgimage,(0,0))
    
    #Draws the snake
    for i in range(0, len(segment_x)):
        screen.blit(img, (segment_x[i], segment_y[i]))

    #Draws the apple
    screen.blit(appleimage, applepos)
        
    #Draws the score text
    scoretext = font.render(str(score), True, (255, 255, 255))
    screen.blit(scoretext, (10, 5))
    
    highscoretext = font.render(str(highscore), True, (255, 255, 255))
    screen.blit(highscoretext, (100, 5))
    
    #Time to update the display
    pygame.display.update()





