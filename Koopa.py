import os
import pygame
from Monster import Monster

class Koopa(Monster):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.is_shell = False
        self.shell_speed = 10
        self.facing_right = False
        self.initial_velocity_x = self.velocity_x  # Store initial velocity
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
            
    def update(self):
        if self.is_alive:
            if self.velocity_x < 0:
                self.facing_right = True
            elif self.velocity_x > 0:
                self.facing_right = False
        
        super().update()
    
    def draw(self, screen, camera):
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
                    
                if not self.facing_right:
                    # Flip the sprite if facing left
                    current_sprite = pygame.transform.flip(current_sprite, True, False)
                    
                # Draw the sprite at the correct position with camera offset
                sprite_rect = current_sprite.get_rect(topleft=(self.rect.x, self.rect.y))
                screen.blit(current_sprite, camera.apply_rect(sprite_rect))
            
    def convert_to_shell(self):
        """Convert Koopa to shell state"""
        self.is_shell = True
        self.current_animation = 'dead'
        self.velocity_x = 0
        
    def kick_shell(self, direction):
        """Kick the shell in a direction"""
        if self.is_shell:
            self.velocity_x = self.shell_speed * direction