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
                
                
class Goomba(Monster):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.death_timer = 0
        self.death_duration = 30
        self.load_sprites()
        
    def clone(self):
        """Create a copy of the Goomba"""
        new_goomba = Goomba(self.rect.x, self.rect.y)
        new_goomba.velocity_x = self.velocity_x
        new_goomba.velocity_y = self.velocity_y
        new_goomba.is_alive = self.is_alive
        new_goomba.current_sprite = self.current_sprite
        new_goomba.animation_speed = self.animation_speed
        new_goomba.current_animation = self.current_animation
        new_goomba.death_timer = self.death_timer
        return new_goomba
        
    def load_sprites(self):
        """Load Goomba-specific sprites"""
        try:
            # Load walking animation
            for i in range(2):  # Assuming 2 walk frames
                sprite_path = os.path.join('assets', 'monsters', f'goomba_walk_{i}.png')
                sprite = pygame.image.load(sprite_path).convert_alpha()
                sprite = pygame.transform.scale(sprite, (64, 64))
                self.sprites['walk'].append(sprite)
                
            # Load death sprite
            sprite_path = os.path.join('assets', 'monsters', 'goomba_dead.png')
            sprite = pygame.image.load(sprite_path).convert_alpha()
            sprite = pygame.transform.scale(sprite, (64, 64))
            self.sprites['dead'].append(sprite)
            
        except pygame.error:
            print("Could not load Goomba sprites. Using placeholder.")
            placeholder = pygame.Surface((64, 64))
            placeholder.fill((139, 69, 19))  # Brown color
            self.sprites['walk'].append(placeholder)
            self.sprites['dead'].append(placeholder)
            
    def update(self):
        """Update Goomba state and handle death animation"""
        if not self.is_alive:
            self.death_timer += 1
            # Don't update position while dying
            return
            
        # Regular update if alive
        super().update()

    def should_remove(self):
        """Check if Goomba should be removed from game"""
        return not self.is_alive and self.death_timer >= self.death_duration
        
    def draw(self, screen, camera):
        """Draw the Goomba"""
        if self.is_alive or self.death_timer < self.death_duration:
            super().draw(screen, camera)
            
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