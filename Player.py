import pygame
import os

class Player:
    def __init__(self, x, y):
        """Initialize player attributes"""
        # Core attributes
        self.rect = pygame.Rect(x, y, 64, 64)
        self.color = (255, 0, 0)  # Temporary color for collision box visualization
        
        # Movement attributes
        self.speed = 5
        self.min_jump_strength = 1
        self.jump_strength = 17
        self.velocity_x = 0
        self.velocity_y = 0
        self.acceleration = 0.5
        self.friction = 0.40
        self.max_speed = 10
        self.jump_force = 0
        
        # State attributes
        self.is_dead = False
        self.can_move = True
        self.is_jumping = False
        self.is_walking = False
        self.facing_right = True
        self.holding_jump = False
        
        # Death animation attributes
        self.death_jump_velocity = -15
        self.is_death_animating = False
        
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
            'dead': [],
        }
        
        try:
            # Load idle animation
            sprite_path = os.path.join('assets', 'player', 'idle.png')
            sprite = pygame.image.load(sprite_path).convert_alpha()
            sprite = pygame.transform.scale(sprite, (64, 64))
            self.sprites['idle'].append(sprite)
            
            # Load walking/running animation
            for i in range(3):  
                sprite_path = os.path.join('assets', 'player', f'run_{i}.png')
                sprite = pygame.image.load(sprite_path).convert_alpha()
                sprite = pygame.transform.scale(sprite, (64, 64))
                self.sprites['walk'].append(sprite)
                
            # Load jump sprite
            sprite_path = os.path.join('assets', 'player', 'jump_up.png')
            sprite = pygame.image.load(sprite_path).convert_alpha()
            sprite = pygame.transform.scale(sprite, (64, 64))
            self.sprites['jump'].append(sprite)
            
            self.current_animation = 'idle'
            self.image = self.sprites['idle'][0]
            
            # Load death sprite
            sprite_path = os.path.join('assets', 'player', 'dead.png')
            sprite = pygame.image.load(sprite_path).convert_alpha()
            sprite = pygame.transform.scale(sprite, (64, 64))
            self.sprites['dead'].append(sprite)
            
        except pygame.error:
            print("Could not load player sprites. Using rectangle placeholder.")
            self.image = pygame.Surface((64, 64))
            self.image.fill(self.color)
            
    def die(self):
        """Initialize player death sequence"""
        if not self.is_death_animating:
            self.is_dead = True
            self.can_move = False
            self.current_animation = 'dead'
            self.current_sprite = 0
            self.velocity_x = 0
            self.velocity_y = self.death_jump_velocity  # Apply initial upward velocity
            self.is_death_animating = True
            # Immediately update to death sprite
            self.image = self.sprites['dead'][0]
    
    def move(self, left, right):
        """Handle horizontal movement with acceleration and friction"""
        
        # Don't allow movement during death animation
        if self.is_death_animating:
            return
        
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
            self.velocity_y = -self.min_jump_strength
            self.is_jumping = True
            self.holding_jump = True
            self.jump_force = self.min_jump_strength
            self.current_animation = 'jump'
            self.current_sprite = 0

    def continue_jump(self):
        """Aumenta a força do salto enquanto o jogador segura o botão"""
        if self.holding_jump and self.jump_force < self.jump_strength:
            self.jump_force += 1  # Incrementa a força do salto
            self.velocity_y = -self.jump_force

    def release_jump(self):
        """Finaliza o salto quando o botão é liberado"""
        self.holding_jump = False
    
    def update(self):
        """Update player state and animation"""
        if self.is_death_animating:
            self.image = self.sprites['dead'][0]
            self.velocity_y += 0.8
            self.rect.y += self.velocity_y
            return
        
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
        
        if self.holding_jump:
            self.continue_jump()
                
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