import pygame as pg

class Command:
    def __init__(self, name, description, action):
        self.name = name
        self.description = description
        self.action = action