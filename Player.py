import pygame as pg
from State import Idle, Walk, Jump, Crouch, Fire
from sprites import MarioSprite

class Player(pg.sprite.Sprite):
    def __init__(self, posX, posY):
        self.posX = posX
        self.posY = posY
        self.velX = 0
        self.velY = 0
        self.playerSprites = MarioSprite() # This will be the sprite sheet that contains all the player sprites
        self.currentSprite = self.playerSprites.mario_images["small_stand"] # This will be the sprite that is currently being displayed / initially the small Mario sprite
        self.rect = self.currentSprite.get_rect()
        self.isSmall = True
        self.state = Idle()

        #self.moviment_states = [Idle, Walk, Jump, Crouch, Fire]
        #self.moviment_transitions = {}
        
    
    def update(self):
        # Aqui nós apenas calculamos a nova posição e fazemos blit na graphics engine
        # print(f"Player position: {self.posX}, {self.posY}")
        pass

    def up(self):
        self.state.update()

    def right(self):
        pass

    def left(self):
        pass

    def down(self):
        pass

    def shoot(self):
        pass
    
    
        