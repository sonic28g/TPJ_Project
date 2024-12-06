import pygame
import os

class Player:
    def __init__(self, x, y):
        """Initialize player attributes"""
        # Core attributes
        self.rect = pygame.Rect(x, y, 50, 50)
        self.color = (255, 0, 0)  # Temporary color for collision box visualization
        
        # Movement attributes
        self.speed = 5
        self.jump_strength = 15
        self.velocity_x = 0
        self.velocity_y = 0
        self.acceleration = 0.2
        self.friction = 0.40
        self.max_speed = 7
        
        # State attributes
        self.is_jumping = False
        self.facing_right = True
        self.is_walking = False
        
        # Animation handling
        self.current_sprite = 0
        self.animation_speed = 0.2
        self.load_sprites()
        
    def load_sprites(self):
        """Load all player sprites"""
        self.sprites = {
            'idle': [],
            'walk': [],
            'jump': [],
        }
        
        try:
            # Load idle animation
            sprite_path = os.path.join('assets', 'player', 'idle.png')
            sprite = pygame.image.load(sprite_path).convert_alpha()
            sprite = pygame.transform.scale(sprite, (50, 50))
            self.sprites['idle'].append(sprite)
            
            # Load walking/running animation
            for i in range(3):  
                sprite_path = os.path.join('assets', 'player', f'run_{i}.png')
                sprite = pygame.image.load(sprite_path).convert_alpha()
                sprite = pygame.transform.scale(sprite, (50, 50))
                self.sprites['walk'].append(sprite)
                
            # Load jump sprite
            sprite_path = os.path.join('assets', 'player', 'jump_up.png')
            sprite = pygame.image.load(sprite_path).convert_alpha()
            sprite = pygame.transform.scale(sprite, (50, 50))
            self.sprites['jump'].append(sprite)
            
            self.current_animation = 'idle'
            self.image = self.sprites['idle'][0]
            
        except pygame.error:
            print("Could not load player sprites. Using rectangle placeholder.")
            self.image = pygame.Surface((50, 50))
            self.image.fill(self.color)
    
    def move(self, left, right):
        """Handle horizontal movement with acceleration and friction"""
        # Apply acceleration based on input
        if right:
            self.velocity_x = min(self.velocity_x + self.acceleration, self.max_speed)
            self.facing_right = True
            self.is_walking = True
        elif left:
            self.velocity_x = max(self.velocity_x - self.acceleration, -self.max_speed)
            self.facing_right = False
            self.is_walking = True
        else:
            self.is_walking = False
            # Apply friction when no input
            if abs(self.velocity_x) < self.friction:
                self.velocity_x = 0
            elif self.velocity_x > 0:
                self.velocity_x -= self.friction
            else:
                self.velocity_x += self.friction
                
        # Update position
        self.rect.x += int(self.velocity_x)
    
    def jump(self):
        """Initiate jump if not already jumping"""
        if not self.is_jumping:
            self.velocity_y = -self.jump_strength
            self.is_jumping = True
            self.current_animation = 'jump'
            self.current_sprite = 0
    
    def update(self):
        """Update player state and animation"""
        if self.is_jumping:
            self.current_animation = 'jump'
            self.current_sprite = 0  # Use jump frame
        elif self.is_walking:
            self.current_animation = 'walk'
            self.current_sprite += self.animation_speed
            if self.current_sprite >= len(self.sprites[self.current_animation]):
                self.current_sprite = 0
        else:
            self.current_animation = 'idle'
            self.current_sprite = 0
                
        # Update current image
        self.image = self.sprites[self.current_animation][int(self.current_sprite)]
        if not self.facing_right:
            self.image = pygame.transform.flip(self.image, True, False)
    
    def draw(self, screen, camera):
        """Draw the player with current animation frame"""
        # Draw collision box for debugging
        # pygame.draw.rect(screen, self.color, camera.apply(self))
        
        # Draw player sprite
        screen.blit(self.image, camera.apply(self))