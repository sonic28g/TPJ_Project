import os
import pygame
from Monster import Monster

class Koopa(Monster):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.is_shell = False
        self.shell_speed = 10
        self.load_sprites()
        
    def clone(self):
        """Create a copy of the Koopa"""
        new_koopa = Koopa(self.rect.x, self.rect.y)
        new_koopa.velocity_x = self.velocity_x
        new_koopa.velocity_y = self.velocity_y
        new_koopa.is_alive = self.is_alive
        new_koopa.current_sprite = self.current_sprite
        new_koopa.animation_speed = self.animation_speed
        new_koopa.current_animation = self.current_animation
        new_koopa.is_shell = self.is_shell
        new_koopa.shell_speed = self.shell_speed
        return new_koopa
        
    def load_sprites(self):
        """Load Koopa-specific sprites"""
        try:
            # Load walking animation
            for i in range(2):  # Assuming 2 walk frames
                sprite_path = os.path.join('assets', 'monsters', f'koopa_walk_{i}.png')
                sprite = pygame.image.load(sprite_path).convert_alpha()
                sprite = pygame.transform.scale(sprite, (64, 64))
                self.sprites['walk'].append(sprite)
                
            # Load shell sprite
            sprite_path = os.path.join('assets', 'monsters', 'koopa_shell.png')
            sprite = pygame.image.load(sprite_path).convert_alpha()
            sprite = pygame.transform.scale(sprite, (64, 64))
            self.sprites['dead'].append(sprite)
            
        except pygame.error:
            print("Could not load Koopa sprites. Using placeholder.")
            placeholder = pygame.Surface((64, 64))
            placeholder.fill((0, 255, 0))  # Green color
            self.sprites['walk'].append(placeholder)
            self.sprites['dead'].append(placeholder)
            
    def convert_to_shell(self):
        """Convert Koopa to shell state"""
        self.is_shell = True
        self.current_animation = 'dead'
        self.velocity_x = 0
        
    def kick_shell(self, direction):
        """Kick the shell in a direction"""
        if self.is_shell:
            self.velocity_x = self.shell_speed * direction