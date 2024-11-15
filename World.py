import pygame as pg
from GameVariables import *
from GameVariables import WINDOW_H, WINDOW_W
from Player import Player
from Camera import Camera
from Utils import loadImage


class World:
    def __init__(self, filename):
        self.level = loadImage(filename)
        self.player = Player(0,0)
        self.camera = Camera(WINDOW_W, WINDOW_H, self.level.get_width(), self.level.get_height())
        self.mobs = []
        self.gameOver = False
        self.lives = 3
        self.coins = 0
        self.time = 0
        self.blocks = []
        
    def update(self):
        # Update player and other entities
        self.player.update()
        for mob in self.mobs:
            mob.update()

        # Update camera
        self.camera.update(self.player.posX, self.player.posY)
        
    def getCameraOffset(self):
        return self.camera.x, self.camera.y
    
    def killMob(self, mob):
        self.mobs.remove(mob)
        
        
