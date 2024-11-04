import pygame as pg

class Player(pg.sprite.Sprite):
    def __init__(self, spritesheet, posX, posY):
        self.posX = posX
        self.posY = posY
        self.velX = 0
        self.velY = 0
        self.currentSprite = None # This will be the sprite that is currently being displayed / initially the small Mario sprite
        self.playerSprites = None # This will be the sprite sheet that contains all the player sprites
        
        self.isSmall = True
        
    
    def update(self):
        # Aqui nós apenas calculamos a nova posição e fazemos blit na graphics engine
        pass
    
    
        