from Monster import Monster
import pygame
import os

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