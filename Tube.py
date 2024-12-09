import pygame as pg
from Settings import GROUND_LEVEL

class Tube(pg.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pg.image.load('assets/level/tube.png').convert_alpha()
        length = (GROUND_LEVEL - y)
        self.image = self.image.subsurface(0,0,64, length)
        self.rect = pg.Rect(x, y, 64, length)

    def draw(self, screen, camera):
        screen.blit(self.image, camera.apply(self))