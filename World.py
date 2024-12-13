import pygame
import os
from Platform import Platform
from Tube import Tube
from Block import BlockInt, BlockBreak, BlockBrick
from MonsterSpawner import MonsterSpawner
from Settings import *
from Koopa import Koopa
from Goomba import Goomba
from Player import Player
from Camera import Camera

class World:
    def __init__(self):
        # Load background
        self.background = self.load_background()
        
        # Score
        self.score = 0
        
        # Lives
        self.lives = 3
        
        # Game Over
        self.is_gameover = False 

        # World elements
        self.platforms = [
            Platform(0, GROUND_LEVEL , 4134, 200), # First Platform
            Platform(4265, GROUND_LEVEL, 890, 200), # Second Platform
            Platform(5345, GROUND_LEVEL, 3829, 200), # Third Platform
            Platform(9305, GROUND_LEVEL, 3323, 200), # Fourth Platform
        ]
        
        # Player
        self.player = Player(300, 780)
        self.spawn_point = (300, 780)
        
        # Camera
        self.camera = Camera(SCREEN_WIDTH, SCREEN_HEIGHT)
        
        self.tubes = [
            Tube(1676,660),
            Tube(2276,600),
            Tube(2756,540),
            Tube(3416,540),
            Tube(9776,660),
            Tube(10736,660),
        ]

        self.blocks = [
            BlockInt(960,540),
            BlockBreak(1200,540),
            BlockInt(1260,540),
            BlockBreak(1320,540),
            BlockInt(1380,540),
            BlockBreak(1440,540),
            BlockInt(1320,300),
            BlockBreak(4620,540),
            BlockInt(4680,540),
            BlockBreak(4740,540),
            BlockBreak(4800,300),
            BlockBreak(4860,300),
            BlockBreak(4920,300),
            BlockBreak(4980,300),
            BlockBreak(5040,300),
            BlockBreak(5100,300),
            BlockBreak(5160,300),
            BlockBreak(5220,300),
            BlockBreak(5460,300),
            BlockBreak(5520,300),
            BlockBreak(5580,300),
            BlockInt(5640,300),
            BlockBreak(5640,540),
            BlockBreak(6000,540),
            BlockBreak(6060,540),
            BlockInt(6360,540),
            BlockInt(6540,540),
            BlockInt(6540,300),
            BlockInt(6720,540),
            BlockBreak(7080,540),
            BlockBreak(7260,300),
            BlockBreak(7320,300),
            BlockBreak(7380,300),
            BlockBreak(7680,300),
            BlockInt(7740,300),
            BlockInt(7800,300),
            BlockBreak(7860,300),
            BlockBreak(7740,540),
            BlockBreak(7800,540),
            BlockBrick(8040,720),
            BlockBrick(8100,660),
            BlockBrick(8160,600),
            BlockBrick(8220,540),
            BlockBrick(8220,600),
            BlockBrick(8220,660),
            BlockBrick(8220,720),
            BlockBrick(8400,540),
            BlockBrick(8400,600),
            BlockBrick(8400,660),
            BlockBrick(8400,720),
            BlockBrick(8460,600),
            BlockBrick(8520,660),
            BlockBrick(8580,720),
            BlockBrick(8880,720),
            BlockBrick(8940,660),
            BlockBrick(9000,600),
            BlockBrick(9060,540),
            BlockBrick(9120,540),
            BlockBrick(9120,600),
            BlockBrick(9120,660),
            BlockBrick(9120,720),
            BlockBrick(9300,540),
            BlockBrick(9300,600),
            BlockBrick(9300,660),
            BlockBrick(9300,720),
            BlockBrick(9360,600),
            BlockBrick(9420,660),
            BlockBrick(9480,720),
            BlockBreak(10080,540),
            BlockBreak(10140,540),
            BlockInt(10200,540),
            BlockBreak(10260, 540),
            BlockBrick(10860,720),
            BlockBrick(10920,660),
            BlockBrick(10980,600),
            BlockBrick(11040,540),
            BlockBrick(11100,480),
            BlockBrick(11160,420),
            BlockBrick(11220,360),
            BlockBrick(11280,300),
            BlockBrick(11340,300),
            BlockBrick(11340,360),
            BlockBrick(11340,420),
            BlockBrick(11340,480),
            BlockBrick(11340,540),
            BlockBrick(11340,600),
            BlockBrick(11340,660),
            BlockBrick(11340,720),
        ]

        # Monster System
        self.monster_spawner = MonsterSpawner()
        self.monsters = []
        self.monster_spawn_points = [
            ('goomba', 1500, GROUND_LEVEL),
            ('koopa', 2500, GROUND_LEVEL),
            ('goomba', 5500, GROUND_LEVEL),
        ]
        
        self.spawn_initial_monsters()

    def load_background(self):
        try:
            bg_path = os.path.join('assets', 'level/level.png')
            original_bg = pygame.image.load(bg_path).convert()
            scale_factor = max(2400 / original_bg.get_width(), 1800 / original_bg.get_height())
            return pygame.transform.scale(original_bg, (
                int(original_bg.get_width() * scale_factor),
                int(original_bg.get_height() * scale_factor)
            ))
        except pygame.error:
            bg = pygame.Surface((2400, 1800))
            bg.fill((135, 206, 235))
            return bg

    def player_die(self):
        """Handle player death"""
        if not self.player.is_death_animating:
            self.lives -= 1
            self.player.die()
            # Reset all monsters to their initial positions
            self.spawn_initial_monsters()
    
    def spawn_initial_monsters(self):
        self.monsters = []
        for monster_type, x, y in self.monster_spawn_points:
            monster = self.monster_spawner.spawn_monster(monster_type, x, y)
            self.monsters.append(monster)

    def update(self):
        # Check for death first
        if self.player.rect.y > GROUND_LEVEL:
            self.player_die()
            
        # If death animation is playing, only update player
        if self.player.is_death_animating:
            self.player.update()
            # Check if player has fallen far enough to reset
            if self.player.rect.y > GROUND_LEVEL + 1500:  # Wait until player falls well below screen
                if self.lives <= 0:
                    self.is_gameover = True
                else:
                    self.player.is_death_animating = False
                    self.player.is_dead = False
                    self.player.can_move = True
                    self.player.rect.x, self.player.rect.y = self.spawn_point
                    self.player.velocity_y = 0
                    self.player.velocity_x = 0
            return
        # List for active monsters
        active_monsters = []
        
        # Update monsters
        for monster in self.monsters:
            monster.update()

            if monster.is_alive:
                # Check for collisions between monster and platforms
                for platform in self.platforms:
                    if monster.rect.colliderect(platform.rect):
                        # [Platform collision logic remains the same]
                        if monster.velocity_y > 0:
                            monster.rect.bottom = platform.rect.top
                            monster.velocity_y = 0
                        elif monster.velocity_y < 0:
                            monster.rect.top = platform.rect.bottom
                            monster.velocity_y = 0
                        elif monster.rect.right > platform.rect.left and monster.rect.left < platform.rect.left:
                            monster.rect.right = platform.rect.left
                            monster.velocity_x *= -1
                        elif monster.rect.left < platform.rect.right and monster.rect.right > platform.rect.right:
                            monster.rect.left = platform.rect.right
                            monster.velocity_x *= -1
                
                # Check for collisions between monster and tubes
                for tube in self.tubes:
                    if monster.rect.colliderect(tube.rect):
                        if monster.velocity_y > 0 and monster.rect.bottom < tube.rect.centery:
                            monster.rect.bottom = tube.rect.top
                            monster.velocity_y = 0
                        elif monster.rect.right > tube.rect.left and monster.rect.left < tube.rect.left:
                            monster.rect.right = tube.rect.left
                            monster.velocity_x *= -1
                        elif monster.rect.left < tube.rect.right and monster.rect.right > tube.rect.right:
                            monster.rect.left = tube.rect.right
                            monster.velocity_x *= -1
                
                # Check for collisions between monster and player
                if monster.rect.colliderect(self.player.rect):
                    # Player is above monster (stomping)
                    if (self.player.velocity_y > 0 and self.player.rect.bottom < monster.rect.centery + 10):
                        if isinstance(monster, Koopa):
                            if not monster.is_shell:
                                # Turn into shell instead of dying
                                monster.convert_to_shell()
                                self.player.velocity_y = -15
                                self.score += 100
                            else:
                                # If already a shell
                                if monster.velocity_x != 0:
                                    # If shell is moving, stop it
                                    monster.velocity_x = 0
                                else:
                                    # If shell is stopped, kick it
                                    direction = 1 if self.player.rect.centerx < monster.rect.centerx else -1
                                    monster.kick_shell(direction)
                                self.player.velocity_y = -10  # Add bounce when kicking shell
                                self.score += 100
                        else:
                            monster.die()
                            self.player.velocity_y = -15  # Bounce player up
                            self.score += 100
                    elif monster.is_alive or (isinstance(monster, Koopa) and monster.is_shell and monster.velocity_x != 0):
                        # Player dies if touching monster from the side or below
                        self.player_die()
                        return
                        
            # Keep the monster if it's still alive, is a Koopa shell, or is playing death animation
            if  monster.is_alive or isinstance(monster, Koopa) or (isinstance(monster, Goomba) and not monster.should_remove()):
                active_monsters.append(monster)
        
        # Update the monsters list to only include active monsters
        self.monsters = active_monsters
        
        # Apply gravity
        self.player.velocity_y += GRAVITY
        self.player.rect.y += self.player.velocity_y

        # Check for collisions between player and platforms
        for platform in self.platforms:
            if self.player.rect.colliderect(platform.rect):
                if self.player.velocity_y > 0 and self.player.rect.right > platform.rect.left + 10 and self.player.rect.left < platform.rect.right - 10:
                    self.player.rect.bottom = platform.rect.top
                    self.player.velocity_y = 0
                    self.player.is_jumping = False
                elif self.player.velocity_y < 0:
                    self.player.rect.top = platform.rect.bottom
                    self.player.velocity_y = 0 
                elif self.player.rect.right > platform.rect.left and self.player.rect.left < platform.rect.left:
                    self.player.rect.right = platform.rect.left
                elif self.player.rect.left < platform.rect.right and self.player.rect.right > platform.rect.right:
                    self.player.rect.left = platform.rect.right

        # Check for collisions between player and blocks
        for block in self.blocks:
            if self.player.rect.colliderect(block.rect):
                # Check if the self.player is landing on the block
                if (
                    self.player.rect.top < block.rect.top
                    and self.player.velocity_y > 0
                    and self.player.rect.right > block.rect.left + 5  # Sufficient horizontal overlap (right side)
                    and self.player.rect.left < block.rect.right - 5  # Sufficient horizontal overlap (left side)
                ):
                    self.player.rect.bottom = block.rect.top
                    self.player.velocity_y = 0
                    self.player.is_jumping = False
                # Check if the self.player hits the bottom of the block
                elif (
                    self.player.rect.bottom > block.rect.bottom
                    and self.player.velocity_y < 0  # Moving upwards
                    and self.player.rect.right > block.rect.left + 5  # Avoid triggering on side collisions
                    and self.player.rect.left < block.rect.right - 5  # Avoid triggering on side collisions
                ):
                    self.player.rect.top = block.rect.bottom
                    self.player.velocity_y = GRAVITY  # Set a positive velocity to simulate falling
                    if isinstance(block, BlockInt):
                        block.hit()

                   
 
                # Check for left-side collision
                elif self.player.rect.right > block.rect.left and self.player.rect.left < block.rect.left:
                    self.player.rect.right = block.rect.left
                # Check for right-side collision
                elif self.player.rect.left < block.rect.right and self.player.rect.right > block.rect.right:
                    self.player.rect.left = block.rect.right

        # Check for collisions between player and tubes
        for tube in self.tubes:
            if self.player.rect.colliderect(tube.rect):
                if (
                    self.player.rect.top < tube.rect.top 
                    and self.player.velocity_y > 0  
                    and self.player.rect.right > tube.rect.left + 5  # Sufficient horizontal overlap (right side)
                    and self.player.rect.left < tube.rect.right - 5  # Sufficient horizontal overlap (left side)
                ):
                    self.player.rect.bottom = tube.rect.top
                    self.player.velocity_y = 0  
                    self.player.is_jumping = False 
                elif self.player.rect.right > tube.rect.left and self.player.rect.left < tube.rect.left:
                    self.player.rect.right = tube.rect.left
                elif self.player.rect.left < tube.rect.right and self.player.rect.right > tube.rect.right:
                    self.player.rect.left = tube.rect.right
        
        # Update player
        self.player.update()
        
        # Prevent monster from moving off screen
        for monster in self.monsters:
            if monster.rect.left < 0:
                monster.rect.left = 0
                monster.velocity_x *= -1
            elif monster.rect.right > self.background.get_width():
                monster.rect.right = self.background.get_width()
                monster.velocity_x *= -1
                
        # Prevent player moving off screen
        if self.player.rect.left < 0:
            self.player.rect.left = 0
            
        # Update camera to follow player
        self.camera.update(self.player)

    def draw(self, screen):
        screen.blit(self.background, self.camera.camera)
        
        for platform in self.platforms:
            if self.camera.camera.colliderect(platform.rect):
                pygame.draw.rect(screen, (139, 69, 19), self.camera.apply_rect(platform.rect))

        for tube in self.tubes:
            tube.draw(screen, self.camera)

        for block in self.blocks:
            block.draw(screen, self.camera)

        for monster in self.monsters:
            monster.draw(screen, self.camera)
            
        self.player.draw(screen, self.camera)