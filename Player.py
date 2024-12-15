import pygame
import os
from Settings import *

class Player:
    def __init__(self, x, y):
        """Initialize player attributes"""
        # Core attributes
        self.rect = pygame.Rect(x, y, 60, 60)
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
        self.visible = True
        
        # Attributes for pole slide animation
        self.is_sliding = False
        self.slide_speed = 3
        self.slide_x = 0
        self.victory_dance = False
        self.slide_sprites = []
        self.victory_sprites = []
        
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
            'flower': [],
            'slide': []
        }
        
        self.big_sprites = {
            'idle': [],
            'walk': [],
            'jump': [],
            'dead': [],
            'level_up': [],
            'flower': [],
            'slide': []
        }
        
        self.flower_sprites = {
            'idle': [],
            'walk': [],
            'jump': [],
            'dead': [],
            'level_up': [],
            'flower': [],
            'slide': []
        }
        
        try:
            # Load small Mario idle sprite
            sprite_path = os.path.join('assets', 'player', 'idle.png')
            sprite = pygame.image.load(sprite_path).convert_alpha()
            sprite = pygame.transform.scale(sprite, (60, 60))
            self.small_sprites['idle'].append(sprite)
            
            # Load walk Mario sprites
            for i in range(3):  
                sprite_path = os.path.join('assets', 'player', f'run_{i}.png')
                sprite = pygame.image.load(sprite_path).convert_alpha()
                sprite = pygame.transform.scale(sprite, (60, 60))
                self.small_sprites['walk'].append(sprite)
                
            # Load jump Mario sprites
            sprite_path = os.path.join('assets', 'player', 'jump_up.png')
            sprite = pygame.image.load(sprite_path).convert_alpha()
            sprite = pygame.transform.scale(sprite, (60, 60))
            self.small_sprites['jump'].append(sprite)
            
            # Load slide sprites
            sprite_path = os.path.join('assets', 'player', 'mario_slide_0.png')
            sprite = pygame.image.load(sprite_path).convert_alpha()
            sprite = pygame.transform.scale(sprite, (60, 60))
            self.small_sprites['slide'].append(sprite)
            
            sprite_path = os.path.join('assets', 'player', 'mario_slide_1.png')
            sprite = pygame.image.load(sprite_path).convert_alpha()
            sprite = pygame.transform.scale(sprite, (60, 60))
            self.small_sprites['slide'].append(sprite)
            
            # Load dead Mario sprites
            sprite_path = os.path.join('assets', 'player', 'dead.png')
            sprite = pygame.image.load(sprite_path).convert_alpha()
            sprite = pygame.transform.scale(sprite, (60, 60))
            self.small_sprites['dead'].append(sprite)
            
            # Load Mario level up sprite
            sprite_path = os.path.join('assets', 'player', 'mario_lvlup.png')
            sprite = pygame.image.load(sprite_path).convert_alpha()
            
            small_sprite = pygame.transform.scale(sprite, (60, 60))
            self.small_sprites['level_up'].append(small_sprite)
            
            big_sprite = pygame.transform.scale(sprite, (60, 120))
            self.big_sprites['level_up'].append(big_sprite)
                    
            # Load big Mario idle sprite
            sprite_path = os.path.join('assets', 'player', 'big_idle.png')
            sprite = pygame.image.load(sprite_path).convert_alpha()
            sprite = pygame.transform.scale(sprite, (60, 120))
            self.big_sprites['idle'].append(sprite)
            
            # Load big walk Mario sprites
            for i in range(3):
                sprite_path = os.path.join('assets', 'player', f'big_run_{i}.png')
                sprite = pygame.image.load(sprite_path).convert_alpha()
                sprite = pygame.transform.scale(sprite, (60, 120))
                self.big_sprites['walk'].append(sprite)
                
            # Load big jump Mario sprites
            sprite_path = os.path.join('assets', 'player', 'big_jump.png')
            sprite = pygame.image.load(sprite_path).convert_alpha()
            sprite = pygame.transform.scale(sprite, (60, 120))
            self.big_sprites['jump'].append(sprite)
                    
            # Create big Mario dead sprite converting the small on
            sprite_path = os.path.join('assets', 'player', 'dead.png')
            sprite = pygame.image.load(sprite_path).convert_alpha()
            sprite = pygame.transform.scale(sprite, (60, 120))
            self.big_sprites['dead'].append(sprite)
            
            # Load big Mario slide sprites
            sprite_path = os.path.join('assets', 'player', 'big_slide_0.png')
            sprite = pygame.image.load(sprite_path).convert_alpha()
            sprite = pygame.transform.scale(sprite, (60, 120))
            self.big_sprites['slide'].append(sprite)
            
            sprite_path = os.path.join('assets', 'player', 'big_slide_1.png')
            sprite = pygame.image.load(sprite_path).convert_alpha()
            sprite = pygame.transform.scale(sprite, (60, 120))
            self.big_sprites['slide'].append(sprite)
            
            # Load flower sprites (already big size)
            sprite_path = os.path.join('assets', 'player', 'flower_idle.png')
            sprite = pygame.image.load(sprite_path).convert_alpha()
            sprite = pygame.transform.scale(sprite, (60, 120))
            self.flower_sprites['idle'].append(sprite)
            
            for i in range(3):
                sprite_path = os.path.join('assets', 'player', f'flower_run_{i}.png')
                sprite = pygame.image.load(sprite_path).convert_alpha()
                sprite = pygame.transform.scale(sprite, (60, 120))
                self.flower_sprites['walk'].append(sprite)
                
            # Add flower jump sprite
            sprite_path = os.path.join('assets', 'player', 'flower_jump.png')
            sprite = pygame.image.load(sprite_path).convert_alpha()
            sprite = pygame.transform.scale(sprite, (60, 120))
            self.flower_sprites['jump'].append(sprite)
                
            # Load flower Mario slide
            sprite_path = os.path.join('assets', 'player', 'flower_slide_0.png')
            sprite = pygame.image.load(sprite_path).convert_alpha()
            sprite = pygame.transform.scale(sprite, (60, 120))
            self.flower_sprites['slide'].append(sprite)
            
            sprite_path = os.path.join('assets', 'player', 'flower_slide_1.png')
            sprite = pygame.image.load(sprite_path).convert_alpha()
            sprite = pygame.transform.scale(sprite, (60, 120))
            self.flower_sprites['slide'].append(sprite)
            
            self.current_animation = 'idle'
            self.sprites = self.small_sprites
            self.image = self.sprites['idle'][0]
            
        except pygame.error as e:
            print(f"Could not load player sprites: {e}")
            self.image = pygame.Surface((60, 60))
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
            self.rect.height = 60
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
        
        # Don't allow movement during death animation or sliding or victory dance
        if self.is_death_animating or self.is_sliding or self.victory_dance:
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
        
        # Don't allow jump during death animation or sliding or victory dance
        if self.is_death_animating or self.is_sliding or self.victory_dance:
            return
        
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
        if self.is_sliding or self.victory_dance:
            self.update_slide_animation()
            return
        
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
                if self.is_jumping:
                    self.image = self.flower_sprites['jump'][0]
                elif self.is_walking:
                    self.current_sprite += self.animation_speed
                    if self.current_sprite >= len(self.flower_sprites['walk']):
                        self.current_sprite = 0
                    self.image = self.flower_sprites['walk'][int(self.current_sprite)]
                else:
                    self.image = self.flower_sprites['idle'][0]
            else:
                # Regular Mario animations
                if self.is_jumping:
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
                
                self.image = self.sprites[self.current_animation][int(self.current_sprite)]
            
            if self.holding_jump:
                self.continue_jump()
        
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
            # First mushroom makes Mario big
            self.is_leveling_up = True
            self.animation_timer = 0
            self.can_move = False
            self.velocity_x = 0
            self.current_animation = 'level_up'
            self.current_sprite = 0
        elif self.is_big and not self.has_flower:
            # Flower makes big Mario into flower Mario
            self.has_flower = True
            self.current_animation = 'flower'
            self.current_sprite = 0
            
    def update_level_up_animation(self):
        self.animation_timer += 1
        
        if self.animation_timer % self.flicker_rate == 0:
            if self.sprites == self.small_sprites:
                self.sprites = self.big_sprites
                self.rect.height = 120
                self.rect.y -= 32
                self.image = self.sprites['idle'][0]  # Use idle sprite for big Mario
            else:
                self.sprites = self.small_sprites
                self.rect.height = 60
                self.rect.y += 32
                self.image = self.sprites['level_up'][0]  # Use level up sprite for small Mario
        
        if self.animation_timer >= self.animation_duration:
            self.is_leveling_up = False
            self.can_move = True
            self.sprites = self.big_sprites
            self.is_big = True
            self.rect.height = 120
            self.current_animation = 'idle'
            
    def start_pole_slide(self, pole_x):
        if not self.is_sliding:
            self.is_sliding = True
            self.slide_x = pole_x - 30  # Offset to grip pole
            self.velocity_x = 0
            self.velocity_y = self.slide_speed
            self.can_move = False
            self.current_sprite = 0
            self.rect.x = self.slide_x  # Immediately snap to pole
            
            # Set correct sprites based on player state
            if self.has_flower:
                self.slide_sprites = self.flower_sprites['slide']  # Use flower slide sprites
            elif self.is_big:
                self.slide_sprites = self.big_sprites['slide']  # Use big Mario slide sprites
            else:
                self.slide_sprites = self.small_sprites['slide']  # Use small Mario slide sprites
            
    def update_slide_animation(self):
        if self.is_sliding:
            self.rect.x = self.slide_x
            if self.rect.bottom < GROUND_LEVEL - 32:
                self.rect.y += self.slide_speed
                self.current_sprite += 0.1
                if self.current_sprite >= len(self.slide_sprites):
                    self.current_sprite = 0
                self.image = self.slide_sprites[int(self.current_sprite)]
            else:
                self.rect.bottom = GROUND_LEVEL - 32  # Lock to ground
                self.is_sliding = False  # Stop sliding
                self.start_victory_walk()  # Start victory sequence
                
        elif self.victory_dance:
            self.facing_right = True
            self.velocity_y += GRAVITY
            self.rect.y += self.velocity_y
            
            if self.rect.x < self.victory_walk_target:
                self.rect.x += 3
                self.current_sprite += 0.1
                if self.current_sprite >= len(self.victory_sprites):
                    self.current_sprite = 0
                self.image = self.victory_sprites[int(self.current_sprite)]
            else:
                self.image = self.sprites['idle'][0]
            
    def start_victory_walk(self):
        """Start victory sequence when flag is collected"""
        self.victory_dance = True
        self.can_move = False
        self.is_sliding = False
        self.velocity_y = -15  # Initial jump velocity
        self.victory_walk_target = self.rect.x + 400  # Target x position
        
        # Set correct sprites based on player state
        if self.has_flower:
            self.victory_sprites = self.flower_sprites['walk']  # Use flower walk sprites
        elif self.is_big:
            self.victory_sprites = self.big_sprites['walk']  # Use big Mario walk sprites
        else:
            self.victory_sprites = self.small_sprites['walk']  # Use small Mario walk sprites
        