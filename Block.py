import pygame as pg
from Settings import GROUND_LEVEL

class Block(pg.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pg.image.load('assets/level/tube.png').convert_alpha()
        self.image = self.image.subsurface(0,0,64,64)
        self.image = pg.transform.scale(self.image, (64*2, 64* 2))
        self.rect = pg.Rect(x, y, 64 * 2, 64 * 2)

    def draw(self, screen, camera):
        screen.blit(self.image, camera.apply(self))