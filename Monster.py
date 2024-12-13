import pygame
import os
from abc import ABC, abstractmethod

class Monster(ABC):
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, 64, 64)
        self.velocity_x = -2  # Default moving left
        self.velocity_y = 0
        self.is_alive = True
        self.sprites = {'walk': [], 'dead': []}
        self.current_sprite = 0
        self.animation_speed = 0.2
        self.current_animation = 'walk'
        
    @abstractmethod
    def clone(self):
        """Create a copy of the monster"""
        pass
        
    def load_sprites(self):
        """Base implementation of load_sprites"""
        pass
        
    def update(self):
        """Update monster position and animation"""
        # Update position
        self.rect.x += self.velocity_x
        self.rect.y += self.velocity_y
        
        # Update animation
        if self.is_alive:
            self.current_sprite += self.animation_speed
            if self.current_sprite >= len(self.sprites[self.current_animation]):
                self.current_sprite = 0
                
        # Apply gravity
        self.velocity_y += 0.8
        
    def die(self):
        """Handle monster death"""
        self.is_alive = False
        self.current_animation = 'dead'
        self.current_sprite = 0
        self.velocity_x = 0
        
    def draw(self, screen, camera):
        """Draw the monster"""
        current_sprite = self.sprites[self.current_animation][int(self.current_sprite)]
        # Flip sprite based on direction
        if self.velocity_x > 0:
            current_sprite = pygame.transform.flip(current_sprite, True, False)
        screen.blit(current_sprite, camera.apply(self))