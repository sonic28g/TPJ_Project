import pygame
import os
from Settings import *

class Player:
    def __init__(self, x, y):
        """Initialize player attributes"""
        # Core attributes
        self.rect = pygame.Rect(x, y, 64, 64)
        self.color = (255, 0, 0)  # Temporary color for collision box visualization
        
        # Movement attributes
        self.speed = 5
        self.velocity_x = 0
        self.velocity_y = 0
        self.jump_force = 0
        
        # State attributes
        self.is_dead = False
        self.can_move = True
        self.is_jumping = False
        self.is_walking = False
        self.facing_right = True
        self.holding_jump = False
        self.is_big = False
        self.has_flower = False
        
        # Animation attributes
        self.is_leveling_up = False
        self.is_taking_damage = False
        self.animation_timer = 0
        self.animation_duration = 40
        self.flicker_rate = 4
        self.invincible = False
        self.invincible_timer = 0
        self.invincible_duration = 120
        self.visible = True  # For damage flicker effect
        
        # Death animation attributes
        self.is_death_animating = False
        
        # Animation handling
        self.current_sprite = 0
        self.animation_speed = 0.2
        self.load_sprites()
        
    def load_sprites(self):
        self.small_sprites = {
            'idle': [],
            'walk': [],
            'jump': [],
            'dead': [],
            'level_up': [],
            'flower': []
        }
        
        self.big_sprites = {
            'idle': [],
            'walk': [],
            'jump': [],
            'dead': [],
            'level_up': [],
            'flower': []
        }
        
        try:
            # Load small Mario sprites
            sprite_path = os.path.join('assets', 'player', 'idle.png')
            sprite = pygame.image.load(sprite_path).convert_alpha()
            sprite = pygame.transform.scale(sprite, (64, 64))
            self.small_sprites['idle'].append(sprite)
            
            # Load walk Mario sprites
            for i in range(3):  
                sprite_path = os.path.join('assets', 'player', f'run_{i}.png')
                sprite = pygame.image.load(sprite_path).convert_alpha()
                sprite = pygame.transform.scale(sprite, (64, 64))
                self.small_sprites['walk'].append(sprite)
                
            # Load jump Mario sprites
            sprite_path = os.path.join('assets', 'player', 'jump_up.png')
            sprite = pygame.image.load(sprite_path).convert_alpha()
            sprite = pygame.transform.scale(sprite, (64, 64))
            self.small_sprites['jump'].append(sprite)
            
            # Load dead Mario sprites
            sprite_path = os.path.join('assets', 'player', 'dead.png')
            sprite = pygame.image.load(sprite_path).convert_alpha()
            sprite = pygame.transform.scale(sprite, (64, 64))
            self.small_sprites['dead'].append(sprite)
            
            # Load Mario level up sprites
            sprite_path = os.path.join('assets', 'player', 'mario_lvlup.png')
            sprite = pygame.image.load(sprite_path).convert_alpha()
            sprite = pygame.transform.scale(sprite, (64, 64))
            self.small_sprites['level_up'].append(sprite)
            
            # Load flower sprites (already big size)
            sprite_path = os.path.join('assets', 'player', 'flower_idle.png')
            sprite = pygame.image.load(sprite_path).convert_alpha()
            self.big_sprites['flower'].append(sprite)
            
            for i in range(3):
                sprite_path = os.path.join('assets', 'player', f'flower_run_{i}.png')
                sprite = pygame.image.load(sprite_path).convert_alpha()
                self.big_sprites['flower'].append(sprite)
            
            # Create big versions
            for animation in self.small_sprites:
                for sprite in self.small_sprites[animation]:
                    self.big_sprites[animation].append(pygame.transform.scale(sprite, (64, 96)))
            
            self.current_animation = 'idle'
            self.sprites = self.small_sprites
            self.image = self.sprites['idle'][0]
            
        except pygame.error as e:
            print(f"Could not load player sprites: {e}")
            self.image = pygame.Surface((64, 64))
            self.image.fill(self.color)
    
    def update_damage_animation(self):
        self.animation_timer += 1
        
        # Flicker visibility
        if self.animation_timer % self.flicker_rate == 0:
            self.visible = not self.visible
        
        # Transition to small at animation end
        if self.animation_timer >= self.animation_duration:
            self.is_taking_damage = False
            self.can_move = True
            self.sprites = self.small_sprites
            self.is_big = False
            self.rect.height = 64
            self.visible = True
            self.current_animation = 'idle'
            self.invincible = True
            self.invincible_timer = 0

    def update_invincibility(self):
        if self.invincible:
            self.invincible_timer += 1
            if self.invincible_timer % self.flicker_rate == 0:
                self.visible = not self.visible
            if self.invincible_timer >= self.invincible_duration:
                self.invincible = False
                self.invincible_timer = 0
                self.visible = True
    
    def take_damage(self):
        if self.has_flower:
            self.has_flower = False
            self.invincible = True
            self.invincible_timer = 0
            return
        
        if self.is_big and not self.is_taking_damage and not self.invincible:
            self.is_taking_damage = True
            self.animation_timer = 0
            self.can_move = False
            self.velocity_x = -5 if self.facing_right else 5
            self.velocity_y = -10
            self.current_animation = 'idle'
            self.current_sprite = 0
    
    def die(self):
        """Initialize player death sequence"""
        if not self.is_death_animating and not self.is_leveling_up:  # Added check for level-up
            self.is_dead = True
            self.can_move = False
            self.current_animation = 'dead'
            self.current_sprite = 0
            self.velocity_x = 0
            self.velocity_y = DEATH_JUMP_VELOCITY
            self.is_death_animating = True
            self.image = self.sprites['dead'][0]
    
    def move(self, left, right):
        """Handle horizontal movement with acceleration and friction"""
        
        # Don't allow movement during death animation
        if self.is_death_animating:
            return
        
        # Apply acceleration based on input
        if right:
            self.velocity_x = min(self.velocity_x + ACCERLERATION, MAX_SPEED)
            self.facing_right = True
            self.is_walking = True
        elif left:
            self.velocity_x = max(self.velocity_x - ACCERLERATION, - MAX_SPEED)
            self.facing_right = False
            self.is_walking = True
        else:
            self.is_walking = False
            # Apply friction when no input
            if abs(self.velocity_x) < FRICITION:
                self.velocity_x = 0
            elif self.velocity_x > 0:
                self.velocity_x -= FRICITION
            else:
                self.velocity_x += FRICITION
                
        # Update position
        self.rect.x += int(self.velocity_x)
    
    def jump(self):
        """Initiate jump if not already jumping"""
        if not self.is_jumping:
            self.velocity_y = -MIN_JUMP_STRENGTH
            self.is_jumping = True
            self.holding_jump = True
            self.jump_force = MIN_JUMP_STRENGTH
            self.current_animation = 'jump'
            self.current_sprite = 0

    def continue_jump(self):
        """Aumenta a força do salto enquanto o jogador segura o botão"""
        if self.holding_jump and self.jump_force < JUMP_STRENGHT:
            self.jump_force += 1  # Incrementa a força do salto
            self.velocity_y = -self.jump_force

    def release_jump(self):
        """Finaliza o salto quando o botão é liberado"""
        self.holding_jump = False
    
    def update(self):
        if self.is_death_animating:
            self.image = self.sprites['dead'][0]
            self.velocity_y += 0.8
            self.rect.y += self.velocity_y
            return
        
        self.update_invincibility()
        
        if self.is_leveling_up:
            self.update_level_up_animation()
            self.image = self.sprites['level_up'][0]
        elif self.is_taking_damage:
            self.update_damage_animation()
        else:
            if self.has_flower:
                self.current_animation = 'flower'
                self.current_sprite += self.animation_speed
                if self.current_sprite >= len(self.sprites[self.current_animation]):
                    self.current_sprite = 0
            elif self.is_jumping:
                self.current_animation = 'jump'
                self.current_sprite = 0
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
            
            self.image = self.sprites[self.current_animation][int(self.current_sprite)]
        
        if not self.facing_right:
            self.image = pygame.transform.flip(self.image, True, False)
    
    def draw(self, screen, camera):
        """Draw the player with current animation frame"""
        # Draw collision box for debugging
        # pygame.draw.rect(screen, self.color, camera.apply(self))
        
        # Draw player sprite
        if self.visible:
            screen.blit(self.image, camera.apply(self))
        
    def grow(self):
        """Handle power-ups (mushroom or flower)"""
        if not self.is_big and not self.is_leveling_up:
            self.is_leveling_up = True
            self.animation_timer = 0
            self.can_move = False
            self.velocity_x = 0
            self.current_animation = 'level_up'
            self.current_sprite = 0
        elif self.is_big and not self.has_flower:
            self.has_flower = True
            self.current_animation = 'flower'
            self.animation_timer = 0
            
    def update_level_up_animation(self):
        self.animation_timer += 1
        
        if self.animation_timer % self.flicker_rate == 0:
            if self.sprites == self.small_sprites:
                self.sprites = self.big_sprites
                self.rect.height = 96
                self.rect.y -= 32
            else:
                self.sprites = self.small_sprites
                self.rect.height = 64
                self.rect.y += 32
        
        if self.animation_timer >= self.animation_duration:
            self.is_leveling_up = False
            self.can_move = True
            self.sprites = self.big_sprites
            self.is_big = True
            self.rect.height = 96
            self.current_animation = 'idle'