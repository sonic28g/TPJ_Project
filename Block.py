import pygame as pg
from Settings import GROUND_LEVEL

class Block(pg.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.rect = pg.Rect(x, y, 64, 60)

    def draw(self, screen, camera):
        screen.blit(self.image, camera.apply(self))

class BlockBreak(Block):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.image = pg.image.load('assets/level/tiles.png').convert_alpha()
        self.image = self.image.subsurface(32*2,0,32,32)
        self.image = pg.transform.scale(self.image, (60, 60))

class BlockInt(Block):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.image = pg.image.load('assets/level/tiles.png').convert_alpha()
        self.image = self.image.subsurface(32*3,0,32,32)
        self.image = pg.transform.scale(self.image, (60, 60))
        self.has_been_hit = False

    def hit(self):
        if not self.has_been_hit:
            self.has_been_hit = True
            self.image = pg.image.load('assets/level/tiles.png').convert_alpha()
            self.image = self.image.subsurface(32*6,0,32,32)
            self.image = pg.transform.scale(self.image, (60, 60))


class BlockBrick(Block):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.image = pg.image.load('assets/level/tiles.png').convert_alpha()
        self.image = self.image.subsurface(32*1,0,32,32)
        self.image = pg.transform.scale(self.image, (60, 60))


    