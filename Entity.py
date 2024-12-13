import pygame
from abc import ABC, abstractmethod

class Entity(ABC):
    def __init__(self, x, y, width, height):
        self.rect = pygame.Rect(x, y, width, height)
        self.velocity_x = 0
        self.velocity_y = 0
        self.is_alive = True

    @abstractmethod
    def update(self):
        """Update the entity's state."""
        pass

    @abstractmethod
    def draw(self, screen, camera):
        """Draw the entity on the screen."""
        pass