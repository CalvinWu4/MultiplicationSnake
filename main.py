# -*- coding: utf-8 -*-
# @Author: Amar Prakash Pandey, Calvin Wu

# import library here
import pygame
import time
import random
from os import path

# contant value initialised
white = (255,255,255)
black = (0,0,0)
red = (255,0,0)
green = (0,155,0)
yellow = (255,255,0)

# display init
display_width = 800
display_height = 600

# game initialization done
pygame.init()
pygame.mixer.init()

# path for the image folder
assets = path.join(path.dirname(__file__), 'assets')
sound_folder = path.join(path.dirname(__file__), 'sounds')

# game display changed
gameDisplay = pygame.display.set_mode((display_width, display_height))

# image loading for both apple and snake
snakeimg = pygame.image.load(path.join(assets + '/snake.png'))
snakebody = pygame.image.load(path.join(assets + '/body.png'))
snaketail = pygame.image.load(path.join(assets + '/tail.png'))
gameicon = pygame.image.load(path.join(assets + '/gameicon.png'))
appleimg = pygame.image.load(path.join(assets + '/apple.png'))
coverimg = pygame.image.load(path.join(assets + '/coverimage.png'))
coverimg = pygame.transform.scale(coverimg,(800,600))

# game name init and display updated
pygame.display.set_caption('Placked | Beyond the Apple')
pygame.display.update()

# updating the game icon in window
pygame.display.set_icon(gameicon)

# controling the no. of frames per sec uisng pygame clock
clock = pygame.time.Clock()

# Frames per second 
FPS = 10

# moving block size
block = 20
appleSize = 30

# snake image direction variable
direction = "right"

# init font object with font size 25 
smallfont = pygame.font.SysFont("comicsansms", 20)
medfont = pygame.font.SysFont("comicsansms", 40)
largefont = pygame.font.SysFont("comicsansms", 70)

# function to pause the game
def pause():
    paused = True
    menu_song = pygame.mixer.music.load(path.join(sound_folder, "menu.ogg"))
    pygame.mixer.music.play(-1)
    while paused:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.QUIT()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    paused = False
                    pygame.mixer.music.fadeout(400)
                if event.key == pygame.K_q:
                    pygame.QUIT()
                    quit()
        gameDisplay.fill(white)
        message_to_display("Paused", black, -80, "large")
        message_to_display("Press [R] to Resume and [Q] to Quit!", black)
        pygame.display.update()

# function to print score
def score(score):
    text = smallfont.render("Score : " + str(score), True, black)
    gameDisplay.blit(text, [2,2])

# function for generating 4 unique random number tuples for multiplication
def getNumPairs():
    return random.sample([[x, y] for x in range(2, 13, 1) for y in range(2, 13, 1)], 4)  # get numbers from 2 to 12

# function for generating points for the apples
# generates 4 unique points that are at least an appleSize distance away from each other
# also makes make sure that the apple is generated at least 10 appleSizes away from the snake's head
def getAppleCoords(current_x, current_y):
    radius = appleSize
    largeRadius = radius * 10
    rangeX = (0, display_width - appleSize)
    rangeY = (0, display_height - appleSize)
    qty = 4  # or however many points you want

    deltas = set()
    # Generate a set of all points within appleSize of the origin, to be used as offsets later
    for x in range(-radius, radius+1):
        for y in range(-radius, radius+1):
            if x*x + y*y <= radius*radius:
                deltas.add((x,y))

    randPoints = []
    excluded = set()
    # Generate a set of all points within 10 appleSizes of the snake head, to be used as offsets later
    for x in range(current_x - largeRadius, (current_x + 1) + largeRadius):
        for y in range(current_y - largeRadius, (current_y + 1) + largeRadius):
            if x*x + y*y <= largeRadius*largeRadius:
                excluded.add((x,y))

    i = 0
    while i<qty:
        x = random.randrange(*rangeX)
        y = random.randrange(*rangeY)
        if (x,y) in excluded: continue
        randPoints.append((x,y))
        i += 1
        excluded.update((x+dx, y+dy) for (dx,dy) in deltas)
    return randPoints


# function to print multiplication problem
def problem(numberOne, numberTwo):
    text = smallfont.render(str(numberOne) + " X " + str(numberTwo) + " = ?", True, black)
    gameDisplay.blit(text, [display_width/2, 2])

# function for putting the number label on the apple
def putNumInApple(num, (x,y)):
    label = smallfont.render(str(num), True, yellow)
    gameDisplay.blit(label, [x,y])

# function for start screen!
def start_screen():
    menu_song = pygame.mixer.music.load(path.join(sound_folder, "menu.ogg"))
    pygame.mixer.music.play(-1)

    # titleTrack.play()
    show_the_welcome_screen = True
    while show_the_welcome_screen:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    show_the_welcome_screen = False
                if event.key == pygame.K_q:
                    pygame.quit()
                    quit()

        gameDisplay.fill(white)
        gameDisplay.blit(coverimg, (0,0))
        message_to_display("Multiplication Snake", green, -120, "large")
        message_to_display("Eat the apples that have the correct solution to the multiplication problem", black, -30)
        message_to_display("The more apples with the correct answer you eat, the longer you get", black, 10)
        message_to_display("If you run into yourself, the boundary, or an apple with the wrong answer you die!",
                           black, 50)
        message_to_display("Press [R] to Play, [SPACE] to Pause and [Q] to Quit", black, 150)

        pygame.display.update()
        clock.tick(15)


# to generate and update snake :P
def snake(block, snakeList):
    # At some point, we may want to rotate the snake's body when it reaches
    # a part where the snake turns
    body = pygame.transform.rotate(snakebody, 0)
    tail = pygame.transform.rotate(snaketail, 0)

    if direction == "right":
        head = pygame.transform.rotate(snakeimg, 270)

    if direction == "left":
        head = pygame.transform.rotate(snakeimg, 90)

    if direction == "up":
        head = snakeimg

    if direction == "down":
        head = pygame.transform.rotate(snakeimg, 180)


    # This method is just working, but not good.
    # Will have to hamake it better and add the snake tail as well.
    gameDisplay.blit(head, (snakeList[-1][0], snakeList[-1][1]))
    for XnY in snakeList[:-1]:
        # gameDisplay.blit(head, (snakeList[-1][0], snakeList[-1][1]))
        pygame.draw.rect(gameDisplay, green, [XnY[0], XnY[1], block, block])


def text_object(msg, color,size):
    if size == "small":
        textSurface = smallfont.render(msg, True, color)
        return textSurface, textSurface.get_rect()

    if size == "medium":
        textSurface = medfont.render(msg, True, color)
        return textSurface, textSurface.get_rect()

    if size == "large":
        textSurface = largefont.render(msg, True, color)
        return textSurface, textSurface.get_rect()

# func to print message on game display
def message_to_display(msg, color, y_displace = 0, size = "small"):
    textSurf , textRect = text_object(msg, color, size)
    textRect.center = (display_width/2), (display_height/2) + y_displace
    gameDisplay.blit(textSurf, textRect)

# game starts here
def gameLoop():
    # global variable direction
    global direction
    global isDead

    # menu sound stops
    pygame.mixer.music.fadeout(600)

    direction = "right"

    # variable init
    gameExit = False
    gameOver = False
    isDead = False

    # snake variables
    snakeList = []
    snakeLength = 1

    # array of apple coordinates tuples
    appleCoords = getAppleCoords(0, 0)

    # apple coordinates tuples
    rightAppleCoords = appleCoords[0]
    wrongApple1Coords = appleCoords[1]
    wrongApple2Coords = appleCoords[2]
    wrongApple3Coords = appleCoords[3]

    # apple x and y coordinates
    rightAppleX = rightAppleCoords[0]
    rightAppleY = rightAppleCoords[1]
    wrongApple1X = wrongApple1Coords[0]
    wrongApple1Y = wrongApple1Coords[1]
    wrongApple2X = wrongApple2Coords[0]
    wrongApple2Y = wrongApple2Coords[1]
    wrongApple3X = wrongApple3Coords[0]
    wrongApple3Y = wrongApple3Coords[1]

    # array of number pair tuples
    numPairs = getNumPairs()

    # number pair tuples
    correctNumPair = numPairs[0]
    wrongNumPair1 = numPairs[1]
    wrongNumPair2 = numPairs[2]
    wrongNumPair3 = numPairs[3]

    start_x = display_width/2
    start_y = display_height/2

    move_to_h = 10
    move_to_v = 0

    while not gameExit :
        if gameOver == True:
            menu_song = pygame.mixer.music.load(path.join(sound_folder, "gameover.ogg"))
            pygame.mixer.music.play(-1)

            while gameOver == True :
                gameDisplay.fill(white)
                message_to_display("Game Over", red, -70, "large")
                text = smallfont.render("Your final score is : " + str(snakeLength), True, black)
                gameDisplay.blit(text, [300,300])
                message_to_display("Press [R] to Play Again and [Q] to quit!", black, 60)
                pygame.display.update()

                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        gameOver = False
                        gameExit = True
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_q:
                            gameExit = True
                            gameOver = False
                        if event.key == pygame.K_r:
                            gameLoop()

        for event in pygame.event.get():
            if event.type  == pygame.QUIT:
                gameExit = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT and move_to_h == 0:
                    direction = "left"
                    move_to_h = -block
                    move_to_v = 0
                elif event.key == pygame.K_RIGHT and move_to_h == 0:
                    direction = "right"
                    move_to_h = block
                    move_to_v = 0
                elif event.key == pygame.K_UP and move_to_v == 0:
                    direction = "up"
                    move_to_v = -block
                    move_to_h = 0
                elif event.key == pygame.K_DOWN and move_to_v == 0:
                    direction = "down"
                    move_to_v = block
                    move_to_h = 0
                elif event.key == pygame.K_SPACE:
                    pause()

        if start_x >= display_width or start_x < 0 or start_y >= display_height or start_y < 0:
            gameOver = True

        start_x += move_to_h
        start_y += move_to_v

        gameDisplay.fill(white)
        gameDisplay.blit(appleimg, rightAppleCoords)
        gameDisplay.blit(appleimg, wrongApple1Coords)
        gameDisplay.blit(appleimg, wrongApple2Coords)
        gameDisplay.blit(appleimg, wrongApple3Coords)


        snakeHead = []
        snakeHead.append(start_x)
        snakeHead.append(start_y)
        snakeList.append(snakeHead)

        if len(snakeList) > snakeLength:
            del snakeList[0]

        score(snakeLength - 1)
        problem(correctNumPair[0], correctNumPair[1])

        putNumInApple((correctNumPair[0] * correctNumPair[1]), rightAppleCoords)
        putNumInApple((wrongNumPair1[0] * wrongNumPair1[1]), wrongApple1Coords)
        putNumInApple((wrongNumPair2[0] * wrongNumPair2[1]), wrongApple2Coords)
        putNumInApple((wrongNumPair3[0] * wrongNumPair3[1]), wrongApple3Coords)

        snake(block, snakeList)
        pygame.display.update()

        # to see if snake has eaten himself or not
        for eachSegment in snakeList[:-1]:
            if eachSegment == snakeHead:
                isDead = True
                snake(block, snakeList)
                pygame.time.delay(1000)
                gameOver = True

        if start_x > rightAppleX and start_x < rightAppleX + appleSize or start_x + block > rightAppleX and \
                start_x + block < rightAppleX + appleSize:
            if start_y > rightAppleY and start_y < rightAppleY + appleSize:

                # Re-generate the apple coordinates
                appleCoords = getAppleCoords(start_x, start_y)
                rightAppleCoords = appleCoords[0]
                wrongApple1Coords = appleCoords[1]
                wrongApple2Coords = appleCoords[2]
                wrongApple3Coords = appleCoords[3]
                rightAppleX = rightAppleCoords[0]
                rightAppleY = rightAppleCoords[1]
                wrongApple1X = wrongApple1Coords[0]
                wrongApple1Y = wrongApple1Coords[1]
                wrongApple2X = wrongApple2Coords[0]
                wrongApple2Y = wrongApple2Coords[1]
                wrongApple3X = wrongApple3Coords[0]
                wrongApple3Y = wrongApple3Coords[1]

                # Regenerate the num pairs
                numPairs = getNumPairs()
                correctNumPair = numPairs[0]
                wrongNumPair1 = numPairs[1]
                wrongNumPair2 = numPairs[2]
                wrongNumPair3 = numPairs[3]

                snakeLength += 1
                menu_song = pygame.mixer.music.load(path.join(sound_folder, "wakka.ogg"))
                pygame.mixer.music.play(0)

            if start_y + block > rightAppleY and start_y + block < rightAppleY + appleSize:

                # Re-generate the apple coordinates
                appleCoords = getAppleCoords(start_x, start_y)
                rightAppleCoords = appleCoords[0]
                wrongApple1Coords = appleCoords[1]
                wrongApple2Coords = appleCoords[2]
                wrongApple3Coords = appleCoords[3]
                rightAppleX = rightAppleCoords[0]
                rightAppleY = rightAppleCoords[1]
                wrongApple1X = wrongApple1Coords[0]
                wrongApple1Y = wrongApple1Coords[1]
                wrongApple2X = wrongApple2Coords[0]
                wrongApple2Y = wrongApple2Coords[1]
                wrongApple3X = wrongApple3Coords[0]
                wrongApple3Y = wrongApple3Coords[1]

                # Regenerate the num pairs
                numPairs = getNumPairs()
                correctNumPair = numPairs[0]
                wrongNumPair1 = numPairs[1]
                wrongNumPair2 = numPairs[2]
                wrongNumPair3 = numPairs[3]

                snakeLength += 1
                menu_song = pygame.mixer.music.load(path.join(sound_folder, "wakka.ogg"))
                pygame.mixer.music.play(0)

        if start_x > wrongApple1X and start_x < wrongApple1X + appleSize or start_x + block > wrongApple1X and \
                start_x + block < wrongApple1X + appleSize:
            if start_y > wrongApple1Y and start_y < wrongApple1Y + appleSize:
                gameOver = True

        if start_x > wrongApple2X and start_x < wrongApple2X + appleSize or start_x + block > wrongApple2X and \
                start_x + block < wrongApple2X + appleSize:
            if start_y > wrongApple2Y and start_y < wrongApple2Y + appleSize:
                gameOver = True

        if start_x > wrongApple3X and start_x < wrongApple3X + appleSize or start_x + block > wrongApple3X and \
                start_x + block < wrongApple3X + appleSize:
            if start_y > wrongApple3Y and start_y < wrongApple3Y + appleSize:
                gameOver = True

        # initialising no. of frames per sec
        clock.tick(FPS)


    pygame.quit()
    # you can signoff now, everything looks good!
    quit()

# # this fuction kicks-off everything 
start_screen()
gameLoop()
