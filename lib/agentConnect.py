import numpy as np
import pygame
from pygame.locals import *

def dataToInput(tileList,spriteList):
    print(tileList,spriteList)

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
