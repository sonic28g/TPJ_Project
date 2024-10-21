import pygame as pg

class Level:
    def __init__(self, filename, levelVersion):
        self.name = "World 1-1"
        self.backgroundImage = self.loadBackgroundImage(filename)
        self.levelVersion = levelVersion

    def loadBackgroundImage(self, filename):
        backgroundImage = pg.image.load (filename)
        if (backgroundImage is None):
            raise Exception("Could not load level background image")
        
        return backgroundImage