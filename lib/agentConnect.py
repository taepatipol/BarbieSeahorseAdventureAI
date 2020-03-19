import numpy as np
import pygame
from pygame.locals import *
import math
from cnst import *
import sys
import os


# utility for fitness
def calculateDistance(x1, y1, x2, y2):
    dist = math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)
    return dist


def calculateFitness(dist):
    try:
        fit = 1 / dist
    except ZeroDivisionError:
        fit = 1
    return fit


def fitnessF(playerPos, levelName):
    if playerPos == None:
        print "fitness function error: can not get player position"
    else:
        # levelSwitcher = {
        #     'Jungle - 1':'jungle1',
        #     'Jungle - 2':'jungle2',
        #     'Jungle - 3':'jungle3',
        #     'Jungle - 4':'jungle4',
        #     'Volcano - 1':'volcano1',
        #     'Volcano - 2':'volcano2',
        #     'Volcano - 3':'volcano3',
        #     '* Bonus *':'bonus',
        #     'Moon - 1':'moon1',
        #     'Moon - 2':'moon2',
        #     'Moon - 3':'moon3',
        #     'Boss':'boss'
        # }
        playerX = int(math.floor(playerPos[0] / TW))
        playerY = int(math.floor(playerPos[1] / TH))
        if levelName == 'Jungle - 1':
            # specify zone
            currentZone = ''
            if playerY <= 32:
                if playerX <= 75:
                    currentZone = 1
                else:
                    currentZone = 3
            else:
                currentZone = 2

            # calc fitness base on distance to door/finish line
            if currentZone == 1:
                fit = calculateFitness(calculateDistance(playerX, playerY, 69, 13))
                return fit
            elif currentZone == 2:
                fit = calculateFitness(calculateDistance(playerX, playerY, 78, 48))
                return fit + 1
            elif currentZone == 3:
                fit = calculateFitness(calculateDistance(playerX, playerY, 156, 27))
                return fit + 2


        elif levelName == 'Jungle - 2':
            pass
    return 0.1


def dataToInput(tileList, spriteList, scXin=0, scYin=0):
    scY = scYin
    scX = scXin
    np.set_printoptions(threshold=sys.maxsize)
    grid = np.zeros((SH / TH, SW / TW))
    # print(grid)
    # hitfile = open(r"D:\study\senior\toba_bubble_kong-1.0\hitgroups.txt","w+")

    for tileCo in tileList:
        if len(tileCo) < 2: continue
        x = tileCo[0] - scX
        y = tileCo[1] - scY
        hitGroups = list(tileCo[2])
        gridX = int(math.floor(x / TW))
        gridY = int(math.floor(y / TH))
        if gridX >= 0 and gridX < SW / TW and gridY >= 0 and gridY < SH / TH:
            if 'solid' not in hitGroups and 'standable' not in hitGroups: continue
            grid[gridY, gridX] = 9
    # hitfile.close()

    for spriteCo in spriteList:
        if len(spriteCo) < 3: continue
        x = spriteCo[0] - scX
        y = spriteCo[1] - scY
        type = spriteCo[2]
        gridX = int(math.floor(x / TW))
        gridY = int(math.floor(y / TH))
        if gridX >= 0 and gridX < SW / TW and gridY >= 0 and gridY < SH / TH:
            dict = {
                'player': 1,
                'parrot': 8,
                'bubble': 2,
                'capsule': 3,
                'door': 4,
                'fireball': 7,
                'fireguy': 8,
                'frog': 8,
                'laser': 7,
                'panda': 8,
                'platform': 3,
                'robo': 8,
                'shootbot': 8,
                'brobo': 8,
                'spikey': 7,
                'blob': 8
            }
            grid[gridY, gridX] = dict.get(type, 99)

    print("----------------------------------\n" + "\r" + str(grid))


def OutputToControl(al):
    # action is [left,right,up,down,jump,shoot]
    actionsList = [0, 1, 0, 0, 0, 0]

    # if left
    if actionsList[0]:  # TODO work with left right event
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


def doAction(action):
    shootEvent = pygame.event.Event(USEREVENT, {'action': action})
    pygame.event.post(shootEvent)
