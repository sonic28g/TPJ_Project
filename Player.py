import pygame as pg

class Player(pg.sprite.Sprite):
    def __init__(self, spritesheet):
        self.posX = 0
        self.posY = 0
        self.velX = 0
        self.velY = 0
        self.currentSprite = None # This will be the sprite that is currently being displayed / initially the small Mario sprite
        self.playerSprites = self.loadPlayerSprites(spritesheet)
        
        self.isSmall = True
        
    def loadPlayerSprites(self, file):
        playerSprites = pg.image.load(file)
        if (playerSprites is None):
            raise Exception("Could not load player sprite")
        
        return playerSprites
    
    def update(self):
        pass
    
    
        