import pygame
import os
from abc import ABC, abstractmethod

class Monster(ABC):
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, 64, 64)
        self.velocity_x = -2
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
        if self.current_animation in self.sprites:
            sprite_list = self.sprites[self.current_animation]
            if sprite_list:  # Check if the list has any sprites
                if len(sprite_list) == 1:
                    # If only one sprite, always use index 0
                    current_sprite = sprite_list[0]
                else:
                    # For multi-frame animations, use modulo to cycle through frames
                    sprite_index = int(self.current_sprite) % len(sprite_list)
                    current_sprite = sprite_list[sprite_index]
                
                # Draw the sprite at the correct position with camera offset
                sprite_rect = current_sprite.get_rect(topleft=(self.rect.x, self.rect.y))
                screen.blit(current_sprite, camera.apply_rect(sprite_rect))