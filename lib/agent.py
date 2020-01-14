import pygame
import time

class Agent:
    def __init__(self,g):
        print("agent online")
        self.game = g
        if g:
            print("agent: game linked to agent")
            print(dir(self.game.input))
            #g.event(pygame.event.Event())
            #newevent = pygame.event.Event(pygame.KEYDOWN,{})
            #g.event.post(newevent) # ERROR has no attribute post

    def test_press_right(self,g):
        self.game.input.right = True
