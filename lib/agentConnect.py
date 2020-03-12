import numpy as np
import pygame
from pygame.locals import *
import math
from cnst import *
import sys
import os

def dataToInput(tileList,spriteList,scXin=0,scYin=0):
    scY = scYin
    scX = scXin
    np.set_printoptions(threshold=sys.maxsize)
    grid = np.zeros((SH/TH,SW/TW))
    #print(grid)
    #hitfile = open(r"D:\study\senior\toba_bubble_kong-1.0\hitgroups.txt","w+")

    for tileCo in tileList:
        if len(tileCo) < 2: continue
        x = tileCo[0] - scX
        y = tileCo[1] - scY
        hitGroups = list(tileCo[2])
        gridX = int(math.floor(x / TW))
        gridY = int(math.floor(y / TH))
        if gridX >= 0 and gridX < SW / TW and gridY >= 0 and gridY < SH / TH:
            if 'player' not in hitGroups:
                for group in hitGroups:
                    #hitfile.write(group)
                grid[gridY,gridX] = 9
    #hitfile.close()

    for spriteCo in spriteList:
        if len(spriteCo) < 3: continue
        x = spriteCo[0]-scX
        y = spriteCo[1]-scY
        type = spriteCo[2]
        gridX = int(math.floor(x/TW))
        gridY = int(math.floor(y/TH))
        if gridX >= 0 and gridX < SW/TW and gridY >= 0 and gridY < SH/TH:
            dict = {
                'player':1,
                'parrot':8,
                'bubble':2,
                'capsule':3,
                'door':4,
                'fireball':7,
                'fireguy':8,
                'frog':8,
                'laser':7,
                'panda':8,
                'platform':3,
                'robo':8,
                'shootbot':8,
                'brobo':8,
                'spikey':7,
                'blob':8
            }
            grid[gridY,gridX] = dict.get(type,99)


    print("----------------------------------\n"+"\r" + str(grid))



def OutputToControl(al):
    # action is [left,right,up,down,jump,shoot]
    actionsList = [0,1,0,0,0,0]

    # if left
    if actionsList[0]: #TODO work with left right event
        leftEvent = pygame.event.Event(USEREVENT, {'action': 'left'})
        pygame.event.post(leftEvent)

    # if right
    if actionsList[1]:
        rightEvent = pygame.event.Event(USEREVENT, {'action': 'right'})
        pygame.event.post(rightEvent)

    # if up
    if actionsList[2]:
        upEvent = pygame.event.Event(USEREVENT, {'action': 'up'})
        pygame.event.post(upEvent)

    # if down
    if actionsList[3]:
        downEvent = pygame.event.Event(USEREVENT, {'action': 'down'})
        pygame.event.post(downEvent)

    # if jump
    if actionsList[4]:
        jumpEvent = pygame.event.Event(USEREVENT, {'action': 'jump'})
        pygame.event.post(jumpEvent)

    # if shoot
    if actionsList[5]:
        shootEvent = pygame.event.Event(USEREVENT, {'action': 'bubble'})
        pygame.event.post(shootEvent)

def mock(action):
    shootEvent = pygame.event.Event(USEREVENT, {'action': action})
    pygame.event.post(shootEvent)