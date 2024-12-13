import pygame
import os
from Platform import Platform
from Tube import Tube
from Block import BlockInt, BlockBreak, BlockBrick
from MonsterSpawner import MonsterSpawner
from Settings import *
from Koopa import Koopa
from Goomba import Goomba

class World:
    def __init__(self):
        # Load and scale background
        self.background = self.load_background()
        
        # Score
        self.score = 0
        
        # Lives
        self.lives = 3

        # World elements
        self.platforms = [
            Platform(0, GROUND_LEVEL , 4134, 200), # First Platform
            Platform(4265, GROUND_LEVEL, 890, 200), # Second Platform
            Platform(5345, GROUND_LEVEL, 3829, 200), # Third Platform
            Platform(9305, GROUND_LEVEL, 3323, 200), # Fourth Platform
        ]
        
        # Player spawn point
        self.spawn_point = (300, 780)
        
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

    def player_die(self, player):
        """Handle player death"""
        if not player.is_death_animating:
            self.lives -= 1
            player.die()
            # Reset all monsters to their initial positions
            self.spawn_initial_monsters()
    
    def spawn_initial_monsters(self):
        self.monsters = []
        for monster_type, x, y in self.monster_spawn_points:
            monster = self.monster_spawner.spawn_monster(monster_type, x, y)
            self.monsters.append(monster)

    def update(self, player):
        # List for active monsters
        active_monsters = []
        
        # First update monsters
        for monster in self.monsters:
            monster.update()

            if monster.is_alive:
                # Apply platform collisions for monsters
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
                
                # Apply pipe collisions for monsters
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
                
                # Check collision with player
                if monster.rect.colliderect(player.rect):
                    # Player is above monster (stomping)
                    if (player.velocity_y > 0 and player.rect.bottom < monster.rect.centery + 10):
                        if isinstance(monster, Koopa):
                            if not monster.is_shell:
                                # Turn into shell instead of dying
                                monster.convert_to_shell()
                                player.velocity_y = -15
                                self.score += 100
                            else:
                                # If already a shell
                                if monster.velocity_x != 0:
                                    # If shell is moving, stop it
                                    monster.velocity_x = 0
                                else:
                                    # If shell is stopped, kick it
                                    direction = 1 if player.rect.centerx < monster.rect.centerx else -1
                                    monster.kick_shell(direction)
                                player.velocity_y = -10  # Add bounce when kicking shell
                                self.score += 100
                        else:
                            monster.die()
                            player.velocity_y = -15  # Bounce player up
                            self.score += 100
                    elif monster.is_alive or (isinstance(monster, Koopa) and monster.is_shell and monster.velocity_x != 0):
                        # Player dies if touching monster from the side or below
                        self.player_die(player)
                        return
                        
            # Keep the monster if it's still alive, is a Koopa shell, or is playing death animation
            if  monster.is_alive or isinstance(monster, Koopa) or (isinstance(monster, Goomba) and not monster.should_remove()):
                active_monsters.append(monster)
        
        # Update the monsters list to only include active monsters
        self.monsters = active_monsters
        
        # Apply gravity
        player.velocity_y += GRAVITY
        player.rect.y += player.velocity_y

        # Check for platform collisions
        for platform in self.platforms:
            if player.rect.colliderect(platform.rect):
                if player.velocity_y > 0 and player.rect.right > platform.rect.left + 10 and player.rect.left < platform.rect.right - 10:
                    player.rect.bottom = platform.rect.top
                    player.velocity_y = 0
                    player.is_jumping = False
                elif player.velocity_y < 0:
                    player.rect.top = platform.rect.bottom
                    player.velocity_y = 0 
                elif player.rect.right > platform.rect.left and player.rect.left < platform.rect.left:
                    player.rect.right = platform.rect.left
                elif player.rect.left < platform.rect.right and player.rect.right > platform.rect.right:
                    player.rect.left = platform.rect.right

        for block in self.blocks:
            if player.rect.colliderect(block.rect):
                # Check if the player is landing on the block
                if (
                    player.rect.top < block.rect.top
                    and player.velocity_y > 0
                    and player.rect.right > block.rect.left + 5  # Sufficient horizontal overlap (right side)
                    and player.rect.left < block.rect.right - 5  # Sufficient horizontal overlap (left side)
                ):
                    player.rect.bottom = block.rect.top
                    player.velocity_y = 0
                    player.is_jumping = False
                # Check if the player hits the bottom of the block
                elif (
                    player.rect.bottom > block.rect.bottom
                    and player.velocity_y < 0  # Moving upwards
                    and player.rect.right > block.rect.left + 5  # Avoid triggering on side collisions
                    and player.rect.left < block.rect.right - 5  # Avoid triggering on side collisions
                ):
                    player.rect.top = block.rect.bottom
                    player.velocity_y = GRAVITY  # Set a positive velocity to simulate falling
                    if isinstance(block, BlockInt):
                        block.hit()

                   
 
                # Check for left-side collision
                elif player.rect.right > block.rect.left and player.rect.left < block.rect.left:
                    player.rect.right = block.rect.left
                # Check for right-side collision
                elif player.rect.left < block.rect.right and player.rect.right > block.rect.right:
                    player.rect.left = block.rect.right

        for tube in self.tubes:
            if player.rect.colliderect(tube.rect):
                if (
                    player.rect.top < tube.rect.top 
                    and player.velocity_y > 0  
                    and player.rect.right > tube.rect.left + 5  # Sufficient horizontal overlap (right side)
                    and player.rect.left < tube.rect.right - 5  # Sufficient horizontal overlap (left side)
                ):
                    player.rect.bottom = tube.rect.top
                    player.velocity_y = 0  
                    player.is_jumping = False 
                elif player.rect.right > tube.rect.left and player.rect.left < tube.rect.left:
                    player.rect.right = tube.rect.left
                elif player.rect.left < tube.rect.right and player.rect.right > tube.rect.right:
                    player.rect.left = tube.rect.right
        
        # Prevent monster from moving off screen
        for monster in self.monsters:
            if monster.rect.left < 0:
                monster.rect.left = 0
                monster.velocity_x *= -1
            elif monster.rect.right > self.background.get_width():
                monster.rect.right = self.background.get_width()
                monster.velocity_x *= -1

    def draw(self, screen, camera):
        screen.blit(self.background, camera.camera)
        for platform in self.platforms:
            if camera.camera.colliderect(platform.rect):
                pygame.draw.rect(screen, (139, 69, 19), camera.apply_rect(platform.rect))

        for tube in self.tubes:
            tube.draw(screen, camera)

        for block in self.blocks:
            block.draw(screen, camera)

        for monster in self.monsters:
            monster.draw(screen, camera)