import numpy as np
import pygame
from pygame.locals import *
import math
from cnst import *
import sys
import os
from collections import deque

class AgentConnect:

    def __init__(self,levelIn):
        grid = np.zeros((SH / TH, SW / TW)).flatten()
        self.gridHistory = deque()
        for i in range(60):
            self.gridHistory.append(grid)
        self.currentFitness = 0
        self.level = levelIn
        if hasattr(self.level,'setAgentCon'):
            self.level.setAgentCon(self)
        self.isGameEnd = 0

    def getGrid(self):
        return self.grid

    def getFitness(self):
        if not hasattr(self.level,'currentFitness'): return None
        return self.level.currentFitness

    def getLvStatus(self):
        if not hasattr(self.level,'status'): return None
        return self.level.status

    def setLevel(self,levelIn):
        self.level = levelIn

    def setGameEnd(self):
        self.isGameEnd = 1

    def getNotImprovedLoop(self):
        if not hasattr(self.level,'notImproved'): return None
        return self.level.notImproved

    def getPlayerPos(self):
        if not hasattr(self.level,'playerPos'): return None
        return self.level.playerPos

    def getPlayerPowerUp(self):
        if not hasattr(self.level,'playerSprite'): return None
        if not hasattr(self.level.playerSprite,'powered_up'): return None
        return self.level.playerSprite.powered_up

    def getScreen(self):
        if hasattr(self.level, 'tilesData'): tileList = self.level.tilesData
        else: return None
        if hasattr(self.level, 'spritesData'): spriteList = self.level.spritesData
        else: return None
        if hasattr(self.level, 'view'):
            scX = self.level.view.left
            scY = self.level.view.top
        else: return None
        # np.set_printoptions(threshold=sys.maxsize)
        # print(grid)
        # hitfile = open(r"D:\study\senior\toba_bubble_kong-1.0\hitgroups.txt","w+")
        currentGrid = np.zeros((SH / TH, SW / TW))

        for tileCo in tileList:
            if len(tileCo) < 2: continue
            x = tileCo[0] - scX
            y = tileCo[1] - scY
            hitGroups = list(tileCo[2])
            gridX = int(math.floor(x / TW))
            gridY = int(math.floor(y / TH))
            if gridX >= 0 and gridX < SW / TW and gridY >= 0 and gridY < SH / TH:
                if 'solid' not in hitGroups and 'standable' not in hitGroups: continue
                currentGrid[gridY, gridX] = 31
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
                    'parrot': 81,
                    'bubble': 20,
                    'capsule': 32,
                    'door': 40,
                    'fireball': 71,
                    'fireguy': 82,
                    'frog': 83,
                    'laser': 72,
                    'panda': 84,
                    'platform': 33,
                    'robo': 85,
                    'shootbot': 86,
                    'brobo': 87,
                    'spikey': 73,
                    'blob': 88
                }
                currentGrid[gridY, gridX] = dict.get(type, 99)

        #if currentGrid is not None: print("----------------------------------\n" + "\r" + str(currentGrid))
        #self.gridHistory.rotate(-1)
        #self.gridHistory[23] = currentGrid.flatten()

        # below will be used if using feedforward nn instead of recurrent
        # out = []
        # i = 0
        # for grid in self.gridHistory:
        #     if i % 10 == 9: out.extend(grid)
        #     i += 1
        
        return currentGrid.flatten()


    def outputToControl(self, al):
        # action is [left,right,jump,shoot]
        actionsList = al
        OPTION = 2
        if OPTION == 1:
            # if left
            if actionsList[0] >= 0.5:
                leftEvent = pygame.event.Event(USEREVENT, {'action': 'left'})
                pygame.event.post(leftEvent)

            # if right
            if actionsList[1] >= 0.5:
                rightEvent = pygame.event.Event(USEREVENT, {'action': 'right'})
                pygame.event.post(rightEvent)

            # if jump
            if actionsList[2] >= 0.5:
                jumpEvent = pygame.event.Event(USEREVENT, {'action': 'jump'})
                pygame.event.post(jumpEvent)

            # if shoot
            if actionsList[3] >= 0.5:
                shootEvent = pygame.event.Event(USEREVENT, {'action': 'bubble'})
                pygame.event.post(shootEvent)
        if OPTION == 2:
            if len(actionsList) < 3: return
            if actionsList[0] <= 0.33:
                leftEvent = pygame.event.Event(USEREVENT, {'action': 'left'})
                pygame.event.post(leftEvent)
            elif actionsList[0] <= 0.66:
                pass
            else:
                rightEvent = pygame.event.Event(USEREVENT, {'action': 'right'})
                pygame.event.post(rightEvent)
            if actionsList[1] >= 0.5:
                jumpEvent = pygame.event.Event(USEREVENT, {'action': 'jump'})
                pygame.event.post(jumpEvent)
            if actionsList[2] >= 0.5:
                shootEvent = pygame.event.Event(USEREVENT, {'action': 'bubble'})
                pygame.event.post(shootEvent)



def doAction(action):
    shootEvent = pygame.event.Event(USEREVENT, {'action': action})
    pygame.event.post(shootEvent)

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

def fitnessF(playerPos, levelName, bossHPIn=6):
    if playerPos is None or not isinstance(playerPos, list) or len(playerPos) != 2:
        print "fitness function error: can not get player position"
        return 0
    else:
        fit = 0.1
        if not isinstance(bossHPIn, int):
            bossHP = 6
        else: bossHP = bossHPIn
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
        if levelName == 'phil_1.tga' or levelName == 'test.tga' or levelName == 'phil_1edited.tga' or levelName == 'phil_1h.tga':
            # specify zone
            currentZone = ''
            if playerY <= 32:
                if playerX <= 87:
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
                return fit+1
            elif currentZone == 3:
                fit = calculateFitness(calculateDistance(playerX, playerY, 156, 27))
                if fit == 3:
                    return  10#10 fitness is finish level
                return fit+2


        elif levelName == 'Jungle - 2' or levelName == 'phil_7.tga':
            door1 = (24,27)
            door2 = (68,24)
            finish = (3,7)
            if playerX <= 44:
                if playerY <= 17:
                    currentZone = 3
                else:
                    currentZone = 1
            else:
                currentZone = 2
            if currentZone == 1:
                fit = calculateFitness(calculateDistance(playerX, playerY, door1[0], door1[1]))
                return fit
            elif currentZone == 2:
                fit = calculateFitness(calculateDistance(playerX, playerY, door2[0], door2[1]))
                return fit+1
            elif currentZone == 3:
                fit = calculateFitness(calculateDistance(playerX, playerY, finish[0], finish[1]))
                return fit+2

        elif levelName == 'Jungle - 3' or levelName == 'tee_1.tga':
            finish = (8,2)
            fit = calculateFitness(calculateDistance(playerX, playerY, finish[0], finish[1]))
            return fit*3

        elif levelName == 'Jungle - 4' or levelName == 'phil_2.tga':
            door1 = (41,6)
            door2 = (54,26)
            finish = (65,5)
            if playerY <= 21:
                if playerX >= 46:
                    currentZone = 3
                else:
                    currentZone = 1
            else:
                currentZone = 2

            if currentZone == 1:
                fit = calculateFitness(calculateDistance(playerX, playerY, door1[0], door1[1]))
                return fit
            elif currentZone == 2:
                fit = calculateFitness(calculateDistance(playerX, playerY, door2[0], door2[1]))
                return fit+1
            elif currentZone == 3:
                fit = calculateFitness(calculateDistance(playerX, playerY, finish[0], finish[1]))
                return fit+2

        elif levelName == 'Volcano - 1' or levelName == 'fydo_1.tga':
            door1 = (18,19)
            finish = (27,8)
            if playerY <= 17:
                currentZone = 2
            else:
                currentZone = 1

            if currentZone == 1:
                fit = calculateFitness(calculateDistance(playerX, playerY, door1[0], door1[1]))
                if fit < 0.01: fit = 0.01
                return fit
            elif currentZone == 2:
                fit = calculateFitness(calculateDistance(playerX, playerY, finish[0], finish[1]))
                if fit < 0.01: fit = 0.01
                return fit+2

        elif levelName == 'Volcano - 2' or levelName == 'tim_1.tga':
            door1 = (19,6)
            finish = (26,8)
            if playerX <= 24:
                currentZone = 1
            else:
                currentZone = 2

            if currentZone == 1:
                fit = calculateFitness(calculateDistance(playerX, playerY, door1[0], door1[1]))
                return fit
            elif currentZone == 2:
                fit = calculateFitness(calculateDistance(playerX, playerY, finish[0], finish[1]))
                return fit+2

        elif levelName == 'Volcano - 3' or levelName == 'pekuja_2.tga':
            finish = (70,14)
            if playerX > 42: zone = 4
            elif playerX > 21:
                if playerY >= 16:
                    zone = 2
                else: zone = 3
            else:
                if playerY >= 16:
                    zone = 1
                else: zone = 0
            if zone == 4:
                fit = calculateFitness(calculateDistance(playerX, playerY, finish[0], finish[1]))
                return fit+2
            elif zone == 0:
                return 0
            elif zone == 1:
                return 0.5
            elif zone == 2:
                return 1
            elif zone == 3:
                return 1.5

        elif levelName == 'Moon - 1' or levelName == 'pekuja_1.tga':
            door1 = (29,70)
            door2 = (61,69)
            door2alt = (52,72)
            door3 = (75,56)
            door3bonus = (103,66)
            finish = (16,23)
            if playerX <= 40:
                if playerY <= 60:
                    currentZone = 4
                else:
                    currentZone = 1
            else:
                if playerX <= 61:
                    currentZone = 2
                elif playerX <= 85:
                    currentZone = 3
                else:
                    currentZone = 3.5

            if currentZone == 1:
                fit = calculateFitness(calculateDistance(playerX, playerY, door1[0], door1[1]))
                return fit/2
            elif currentZone == 2:
                fit1 = calculateFitness(calculateDistance(playerX, playerY, door2[0], door2[1]))
                fit2 = calculateFitness(calculateDistance(playerX, playerY, door2alt[0], door2alt[1]))
                if fit1 > fit2:
                    return fit1/2 + 0.5
                else: return fit2/2 + 0.5
            elif currentZone == 3:
                fit = calculateFitness(calculateDistance(playerX, playerY, door3[0], door3[1]))
                return fit+1
            elif currentZone == 3.5:
                fit = calculateFitness(calculateDistance(playerX, playerY, door3bonus[0], door3bonus[1]))
                return fit+1
            elif currentZone == 4:
                fit = calculateFitness(calculateDistance(playerX, playerY, finish[0], finish[1]))
                return fit+2

        elif levelName == "Moon - 2" or levelName == "phil_5.tga":
            doorHiddenIn = (35,68)
            doorHiddenOut = (29,56)
            door2 = (60,44)
            finish = (14,38)

            if playerX > 33:
                if playerY <= 54:
                    currentZone = 3
                else:
                    currentZone = 1
            else:
                if playerY >= 50:
                    currentZone = 2
                else:
                    currentZone = 4

            if currentZone == 1:
                fit = calculateFitness(calculateDistance(playerX, playerY, doorHiddenIn[0], doorHiddenIn[1]))
                return fit / 2
            elif currentZone == 2:
                fit = calculateFitness(calculateDistance(playerX, playerY, doorHiddenOut[0], doorHiddenOut[1]))
                return fit / 2 + 0.5
            elif currentZone == 3:
                fit = calculateFitness(calculateDistance(playerX, playerY, door2[0], door2[1]))
                return fit + 1
            elif currentZone == 4:
                fit = calculateFitness(calculateDistance(playerX, playerY, finish[0], finish[1]))
                return fit + 2

        elif levelName == "Moon - 3" or levelName == "phil_9.tga":
            finish = (70,66)
            fit = calculateFitness(calculateDistance(playerX, playerY, finish[0], finish[1]))
            return fit

        elif levelName == "Boss" or levelName == "boss_1.tga":
            fit = 6 - bossHP
            door = (2,18)
            if bossHP == 3:
                if playerY >= 17:
                    fit = calculateFitness(calculateDistance(playerX, playerY, door[0], door[1]))
                    fit += 3 + fit
                else:
                    fit = 3.99
            return fit/2


    return fit
