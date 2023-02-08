
#import pdb; 
#pdb.set_trace()

import pygame, sys, math
import Bird, Pipe
from pygame.locals import *

WIDTH, HEIGHT = 336,600

pygame.init()

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("FlappyBird")

clock = pygame.time.Clock()

digits = [
    pygame.image.load("sprites/0.png"),
    pygame.image.load("sprites/1.png"),
    pygame.image.load("sprites/2.png"),
    pygame.image.load("sprites/3.png"),
    pygame.image.load("sprites/4.png"),
    pygame.image.load("sprites/5.png"),
    pygame.image.load("sprites/6.png"),
    pygame.image.load("sprites/7.png"),
    pygame.image.load("sprites/8.png"),
    pygame.image.load("sprites/9.png")
]

pipeSprite = pygame.image.load("sprites/pipe-green.png").convert_alpha()
pipeShaft = pygame.image.load("sprites/shaft.png").convert_alpha()

baseSprite = pygame.image.load("sprites/base.png").convert_alpha()
baseSprite = pygame.transform.scale(baseSprite, (WIDTH, 112)).convert_alpha()

bg = pygame.image.load("sprites/background-day.png")
bg = pygame.transform.scale(bg, (WIDTH, HEIGHT))

message = pygame.image.load("sprites/message.png")
gameOverScreen = pygame.image.load("sprites/gameover.png")

birdSpriteList = [
    pygame.image.load("sprites/redbird-downflap.png"),
    pygame.image.load("sprites/redbird-midflap.png"),
    pygame.image.load("sprites/redbird-upflap.png")
]

flapSound = pygame.mixer.Sound("audio/wing.wav")
pointSound = pygame.mixer.Sound("audio/point.wav")
hitSound = pygame.mixer.Sound("audio/hit.wav")
dieSound = pygame.mixer.Sound("audio/die.wav")

def Reset():
    scoreDigits = [0,0,0]
    birdSprite = birdSpriteList[0]
    currentAnimation = 0

    birdAngle = 0

    velocity = -1

    bird = Bird.Bird(WIDTH, HEIGHT, (WIDTH / 2) - (birdSprite.get_width() / 2) - 100)

    pipes = []
    base = [Pipe.Base(WIDTH, HEIGHT, 0), Pipe.Base(WIDTH, HEIGHT, WIDTH)]

    frameCount = 0

    hasPlayedDieSound = False
    return scoreDigits, birdSprite, currentAnimation, birdAngle, velocity, bird, pipes, base, frameCount, hasPlayedDieSound
    
#scoreDigits = [0,0,0]
#birdSprite = birdSpriteList[0]
#currentAnimation = 0

#birdAngle = 0

#velocity = -1

#bird = Bird.Bird(WIDTH, HEIGHT, (WIDTH / 2) - (birdSprite.get_width() / 2) - 100)

#pipes = []
#base = [Pipe.Base(WIDTH, HEIGHT, 0), Pipe.Base(WIDTH, HEIGHT, WIDTH)]

#frameCount = 0
scoreDigits, birdSprite, currentAnimation, birdAngle, velocity, bird, pipes, base, frameCount, hasPlayedDieSound = Reset()

while True:

    clock.tick(60)

    frameCount+=1

    if (frameCount % 6 == 0) :
        currentAnimation += 1
        if (currentAnimation >= len(birdSpriteList)):
            currentAnimation = 0

    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        if event.type == KEYDOWN:
            if bird.isWaiting:
                bird.Start()
                pipes = [Pipe.Pipe(WIDTH, HEIGHT), Pipe.Pipe(WIDTH * 3 / 2, HEIGHT)]

            else:
                bird.Jump()
                pygame.mixer.Sound.play(flapSound)
            
            if not bird.alive:scoreDigits, birdSprite, currentAnimation, birdAngle, velocity, bird, pipes, base, frameCount, hasPlayedDieSound = Reset()

    bird.Update(velocity, frameCount, (WIDTH / 2) - ((birdSprite.get_height())/ 2))

    for i in range(0,len(base)):
        screen.blit(bg, (base[i].x, 0))

    for i in range(0,len(pipes)):
        if pipes[i].Update(velocity):
            pipes[i] = Pipe.Pipe(WIDTH, HEIGHT)
        pipeBot = pipeSprite
        pipeTop = pygame.transform.rotate(pipeSprite, 180)
        pipeFiller = pygame.transform.scale(pipeShaft, (52, HEIGHT))
        screen.blit(pipeFiller, (pipes[i].x, pipes[i].bottomHeight))
        screen.blit(pygame.transform.rotate(pipeFiller, 180), (pipes[i].x, pipes[i].topHeight - pipeFiller.get_height()))
        screen.blit(pipeTop, (pipes[i].x, pipes[i].topHeight - pipeSprite.get_height()))
        screen.blit(pipeBot, (pipes[i].x, pipes[i].bottomHeight))

        if (bird.collisionDetect(pipes[i], velocity, HEIGHT - baseSprite.get_height(), birdSpriteList[0].get_width() / 2)):
            velocity -= 0.1
            pygame.mixer.Sound.play(pointSound)
    
    for i in range(0,len(base)):
        if (base[i].Update(WIDTH, velocity)):
            base[i] = Pipe.Base(WIDTH, HEIGHT, WIDTH)
        screen.blit(baseSprite, (base[i].x, HEIGHT - baseSprite.get_height()))


    birdSprite = birdSpriteList[currentAnimation]
    birdAngle = math.atan(bird.direction[1] / bird.direction[0]) * 180 / math.pi
    while (birdAngle < 0 or birdAngle > 360):
        if (birdAngle < 0):
            birdAngle += 360
        if birdAngle > 360:
            birdAngle -= 360
    birdSprite = pygame.transform.rotate(birdSprite, birdAngle)

    screen.blit(birdSprite, (bird.x, bird.currentHeight - (birdSprite.get_height() / 2)))

    scoreDigits[0] = int(bird.score / 100)
    scoreDigits[1] = int((bird.score - (scoreDigits[0]*100)) / 10)
    scoreDigits[2] = int((bird.score - (scoreDigits[1]*10)))

    for i in range(0,3):
        if (not bird.isWaiting):screen.blit(digits[scoreDigits[i]], ((WIDTH / 2) - digits[scoreDigits[i]].get_width() * 3 / 2 + i*digits[scoreDigits[i]].get_width(), 50))

    if bird.isWaiting:
        screen.blit(message, ((WIDTH / 2) - (message.get_width() / 2),50))
    if not bird.alive:
        if not hasPlayedDieSound:
            pygame.mixer.Sound.play(hitSound)
            pygame.mixer.Sound.play(dieSound)
            hasPlayedDieSound = True

        screen.blit(gameOverScreen, ((WIDTH / 2) - (gameOverScreen.get_width() / 2), 100))

    pygame.display.flip()