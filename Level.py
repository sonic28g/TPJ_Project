import pygame as pg
from HelperFunctions import loadImage

class Level:
    def __init__(self, filename, name, levelVariant):
        self.name = name
        self.backgroundImage = loadImage(filename)
        self.levelVariant = levelVariant