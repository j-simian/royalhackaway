import pygame
from utils import *
from funs import *
from options import *
from player import *

def initEntities(state):
    entities = {}
    p1 = Player(0, state)
    p2 = Player(1, state)
    p1.x, p2.x = 200, 600
    p1.y, p2.y = GROUNDHEIGHT, GROUNDHEIGHT
    entities["p1"], entities["p2"] = p1, p2
    return entities


def dashAvailable(accuracy, player, frame):
    return accuracy == 'perfect' and (player.lastdash+1/2<frame or player.lastdashdir!=player.moving)


def handlePress(event, timer, player, control, state, enemy, entities):
    (accuracy,whichNote)=timer.onRhythm(False)
    frame = timer.getHalfFrame()
    available = dashAvailable(accuracy, player, frame)
    if available and event.key in [control['left'], control['right']]:
        print("wow!")
        player.lastdash = frame
        player.lastdashdir = player.moving
        player.dash+=MAXVELX*DASHRATIO
    if event.key == control['left']:
        player.moving = -1
    if event.key == control['right']:
        player.moving = 1
    if event.key == control['up']:
        player.jumping = 0.6
    if event.key == control['attack']:
        if player.canAttack == True and player.stun <= 0:
            if player.touchingFloor:
                if player.combo == 1 and (frame-player.lasthitframe == 1/2):
                    player.attackType = "light2"
                    player.combo+=1
                elif player.combo == 1 and (frame-player.lasthitframe == 1):
                    player.attackType = "heavy"
                    player.combo=0
                elif player.combo == 2 and (frame-player.lasthitframe == 1/2):
                    player.attackType = "light3"
                    player.combo=0
                else:
                    player.attackType = "light1"
                    player.combo=1
                player.lasthitframe = frame
            else:
                player.attackType = "heavy"
            player.mystate = "charge"
            player.charging = CHARGETIME
            player.canAttack = False

def handleRelease(event, player, control):
    if event.key == control['left'] and player.moving == -1:
        player.moving = 0
        if pygame.key.get_pressed()[control['right']]:
            player.moving = 1
    if event.key == control['right'] and player.moving == 1:
        player.moving = 0
        if pygame.key.get_pressed()[control['left']]:
            player.moving = -1
    if event.key == control['up'] and player.jumping > 0:
        player.jumping = 0

def handleMove(player, control, event, timer, state, enemy, entities):
    if event.type == pygame.KEYDOWN:
        handlePress(event, timer, player, control, state, enemy, entities)
    if event.type == pygame.KEYUP:
        handleRelease(event, player, control)


