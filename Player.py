import pygame as pg
from State import Idle, Walk, Jump, Crouch, Fire
from sprites import MarioSprite
from GameVariables import PLAYER_SCALE, ACCELERATION, TOP_SPEED
from FSM import FSM

class Player(pg.sprite.Sprite):
    def __init__(self, posX, posY):
        self.posX = posX
        self.posY = posY
        self.velX = 0
        self.velY = 0
        self.playerSprites = MarioSprite() # This will be the sprite sheet that contains all the player sprites
        self.currentSprite = self.playerSprites.mario_images["small_stand"] # This will be the sprite that is currently being displayed / initially the small Mario sprite
        self.rect = pg.Rect(self.posX, self.posY, PLAYER_SCALE, PLAYER_SCALE)
        self.isSmall = True

        self.leftTurned = False
        self.walkingSpriteInd = 0
        self.walkingSprites = [self.playerSprites.mario_images["small_run_1"], self.playerSprites.mario_images["small_run_2"], self.playerSprites.mario_images["small_run_3"]]
        self.FC = 0


        self.state = Idle()

        self.moviment_states = [Idle, Walk, Jump, Crouch, Fire]
        self.moviment_transitions = {}

        self.fsm = FSM(self.moviment_states, self.moviment_transitions)
        
    
    def update(self):
        # Aqui nós apenas calculamos a nova posição e fazemos blit na graphics engine
        # print(f"Player position: {self.posX}, {self.posY}")
        self.posX += self.velX
        self.rect = pg.Rect(self.posX, self.posY, PLAYER_SCALE, PLAYER_SCALE)
        
        # DEADZONE
        if(self.velX < ACCELERATION and self.velX > -ACCELERATION):
            self.velX = 0
            self.currentSprite = self.playerSprites.mario_images["small_stand"]
            self.WalkingSprite = 0


        self.currentSprite = pg.transform.flip(self.currentSprite, self.leftTurned, False)
            

    def up(self):
        pass 

    def right(self):
        if self.velX < TOP_SPEED:
            self.velX += ACCELERATION
        if(self.velX < 0):
            self.currentSprite = self.playerSprites.mario_images["small_turn"]
            self.leftTurned = True
        else:
            self.currentSprite = self.playerSprites.mario_images["small_stand"]
            self.leftTurned = False

    def left(self):
        if self.velX > -TOP_SPEED:
            self.velX -= ACCELERATION
        if(self.velX > 0):
            self.currentSprite = self.currentSprite = self.playerSprites.mario_images["small_turn"]
        else:
            self.currentSprite = self.playerSprites.mario_images["small_stand"]
            self.leftTurned = True


    def down(self):
        pass

    def shoot(self):
        pass

    def idle(self):
        if self.velX > 0:
            self.velX -= ACCELERATION
        elif self.velX < 0:
            self.velX += ACCELERATION


    
    
        