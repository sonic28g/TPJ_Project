import pygame

from Player import Player
from GameVariables import FPS


class Game:
    def __init__(self):
        self.running = True
        self.clock = pygame.time.Clock()


    def start(self):
        while self.running:
            self.input()
            self.update()
            self.render()
            self.clock.tick(FPS)

    def input(self):
        pass

    def update(self):
        pass

    def render(self):
        pass 
    