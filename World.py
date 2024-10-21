import pygame as pg
from GameVariables import *
from Level import Level
from PhysicsEngine import PhysicsEngine
from Player import Player
from Camera import Camera
from Sound import Sound


class World:
    def __init__(self):
        self.level = Level()
        self.physicsEngine = PhysicsEngine()
        self.player = Player()
        self.mobs = []
        self.events = []
        self.camera = Camera()
    
        
