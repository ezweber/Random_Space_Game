#Made by ezweber

import pygame
from pygame import mixer

import random
import math
import time

pygame.init()

#window size
screen = pygame.display.set_mode((800,600))

#window name and icon
pygame.display.set_caption("Space Game")
icon = pygame.image.load('icon.png')
pygame.display.set_icon(icon)

#background image
background = pygame.image.load('background.png')

#background music
mixer.music.load('background.wav')
mixer.music.play(-1)
    
def startfunc():
    #player
    global player
    global playerx
    global playery
    global playerx_change

    player = pygame.image.load('player.png')
    playerx = screen.get_width() / 2
    playery = 480
    playerx_change = 0

    #enemy
    global enemy
    global enemyx
    global enemyy
    global enemyx_change
    global enemyy_change
    global num_of_enemys
    
    enemy = []
    enemyx = []
    enemyy = []
    enemyx_change = []
    enemyy_change = []
    num_of_enemys = 6

    for i in range(num_of_enemys):
        enemy_pic = random.randint(1,2)
        if enemy_pic == 1:
            enemy.append(pygame.image.load('enemy.png'))
        else:
             enemy.append(pygame.image.load('enemy2.png'))
             
        enemyx.append(random.randint(0, screen.get_width()-65)) 
        enemyy.append(random.randint(50, 150)) 
        enemyx_change.append(3)
        enemyy_change.append(30)
        
    #bullet
    global bullet
    global bulletx
    global bullety
    global bulletx_change
    global bullety_change
    global bullet_state

    bullet = pygame.image.load('bullet.png')
    bulletx = 0
    bullety = playery
    bulletx_change = 0
    bullety_change = 7
    bullet_state = "ready"

    #astroid
    global astroid
    global astroidx
    global astroidy
    global astroidy_change

    astroid = pygame.image.load('astroid.png')
    astroidx = random.randint(0, screen.get_width()-65)
    astroidy = 0
    astroidy_change = 5

#score
score_value = 0
font = pygame.font.Font('freesansbold.ttf',32)
textx = 10
texty = 10

def show_score(x,y):
    score = font.render("Score :" + str(score_value),True, (255,255,255))
    screen.blit(score, (x,y))

#game over text
game_over_font = pygame.font.Font('freesansbold.ttf',64)

def game_over_text():
    over_text = game_over_font.render("GAME OVER", True, (255,255,255))
    screen.blit(over_text, (200, 250))

quit_font = pygame.font.Font('freesansbold.ttf',32)

def game_quit_text():
    quit_text = quit_font.render("Q to quit", True, (255,255,255))
    screen.blit(quit_text, (330, 340))

def game_restart_text():
    quit_text = quit_font.render("E to restart", True, (255,255,255))
    screen.blit(quit_text, (315, 380))

def iscollision(enemyx,enemyy,bulletx,bullety):
    distance = math.sqrt((math.pow(enemyx-bulletx,2))+(math.pow(enemyy-bullety,2)))
    if distance < 27:
        return True
    else:
        return False

def astroid_collision(astroidx,astroidy,playerx,playery):
    distance = math.sqrt((math.pow(astroidx-playerx,2))+(math.pow(astroidy-playery,2)))
    if distance < 35:
        return True
    else:
        return False
    
def playerfunc(x,y):
    screen.blit(player, (x, y))

def fire_bullet(x,y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bullet, (x + 16, y + 10))

def astroidfunc(x,y):
    screen.blit(astroid, (x, y))

def enemyfunc(x,y,i):
            screen.blit(enemy[i], (x, y))
    
#preset variables
running = True
start = False
gameover = False
played_hit_sound = False

#Game loop
while running:

    #background
    screen.fill((0,0,0))
    screen.blit(background, (0,0))

    #events
    for event in pygame.event.get():
        #quit
        if event.type == pygame.QUIT:
            running = False
        #keystrokes
        if event.type ==  pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    start = True
                    startfunc()
                if event.key == pygame.K_LEFT:
                    playerx_change = -4
                if event.key == pygame.K_RIGHT:
                    playerx_change = 4
                if event.key == pygame.K_a:
                    playerx_change = -4
                if event.key == pygame.K_d:
                    playerx_change = 4
                if event.key == pygame.K_SPACE:
                    if bullet_state == "ready":
                        bullet_sound = mixer.Sound('laser.wav')
                        bullet_sound.play()
                        bulletx = playerx
                        fire_bullet(playerx, bullety)
                if event.key == pygame.K_q and gameover == True:
                    running = False
                if event.key == pygame.K_e and gameover == True:
                    startfunc()
                    gameover = False
                    score_value = 0
                                        
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT or event.key == pygame.K_a or event.key == pygame.K_d:
                playerx_change = 0


    if start:

        #moving the player        
        playerx += playerx_change

        #player boundary
        if playerx <= 0:
            playerx = 0
        elif playerx >= 736:
            playerx = 736

        #moving the enemy 
        for i in range(num_of_enemys):

            #game over check
            if enemyy[i] > 440:
                gameover = True
                break

            enemyx[i] += enemyx_change[i]

            #enemy boundary
            if enemyx[i] <= 0:
                enemyx_change[i] = 3
                enemyy[i] += enemyy_change[i]
            elif enemyx[i] >= 736:
                enemyy[i] += enemyy_change[i]
                enemyx_change[i] = -3 

            #collision
            collision = iscollision(enemyx[i],enemyy[i],bulletx,bullety)
            if collision and bullet_state == "fire":
                hit_sound = mixer.Sound('explosion.wav')
                hit_sound.play()
                bullety = 480
                bullet_state ="ready"
                score_value += 1
                print(score_value)
                enemyx[i] = random.randint(0, (screen.get_width()-65))
                enemyy[i] = random.randint(50, 150)

            #call enemy function
            if gameover == False:
                enemyfunc(enemyx[i], enemyy[i], i)

        #bullet movement
        if bullety <= 0:
            bullety = playery
            bullet_state = "ready"
        if bullet_state == "fire":
            fire_bullet(bulletx, bullety)
            bullety -= bullety_change

        #astroid movement
        astroidy += astroidy_change

        astroidfall = random.randint(1000, 6000)
        if astroidy >= astroidfall:
            astroidy = 0
            astroidx = random.randint(0, screen.get_width()-65)

        if astroid_collision(astroidx,astroidy,playerx,playery):
            gameover = True
            if played_hit_sound == False:
                hit_sound = mixer.Sound('explosion.wav')
                hit_sound.play()
                played_hit_sound = True

        #call functions
        if gameover == False:
            astroidfunc(astroidx,astroidy)

        if gameover:
            game_over_text()
            game_quit_text()
            game_restart_text()

        show_score(textx,texty)      
        playerfunc(playerx, playery)

    else:
        #start screen text
        startscreenfont = pygame.font.Font('freesansbold.ttf',64)

        startscreentext = startscreenfont.render("Press Q to start", True, (255,255,255))
        screen.blit(startscreentext, (150, 250))

        helpscreenfont = pygame.font.Font('freesansbold.ttf',32)

        helpscreentext = helpscreenfont.render("Press H for help", True, (255,255,255))
        screen.blit(helpscreentext, (260, 315))

    #update screen
    pygame.display.update()

