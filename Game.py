import pygame
import sys
import os
from Tube import Tube
from Camera import Camera
from Player import Player
from Platform import Platform
from MainMenu import MainMenu
from PauseMenu import PauseMenu
from MonsterSpawner import MonsterSpawner
from Goomba import Goomba
from Koopa import Koopa
from Settings import *
from Block import *

class Game:
    def __init__(self):
        # Initialize Pygame
        pygame.init()
        
        # UI font
        self.font = pygame.font.Font(None, 36)
        
        # Game state variables
        self.score = 0
        self.lives = 3

        # Screen setup
        self.screen_width = SCREEN_WIDTH
        self.screen_height = SCREEN_HEIGHT
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        pygame.display.set_caption(GAME_TITLE)
        
        # Initialize Monster System
        self.monster_spawner = MonsterSpawner()
        self.monsters = []
        
        # Store initial monster spawn points
        self.monster_spawn_points = [
            ('goomba', 1500, 600),
            ('goomba', 2500, 600),
            ('koopa', 3500, 600),
            ('goomba', 4500, 600)
        ]
        
        # Spawn initial monsters
        self.spawn_initial_monsters()
        
        # Game state and Menus
        self.game_state = MENU
        self.menu = MainMenu(self.screen_width, self.screen_height)
        self.pause_menu = PauseMenu(self.screen_width, self.screen_height)

        # Load and scale background image properly
        try:
            # Load original background
            background_path = os.path.join('assets', 'level/level.png')
            original_background = pygame.image.load(background_path).convert()
            
            # Calculate scaling to maintain aspect ratio
            bg_width = original_background.get_width()
            bg_height = original_background.get_height()
            
            # Determine scale factor to match game world size
            scale_factor = max(2400 / bg_width, 1800 / bg_height)
            self.scale_factor = scale_factor
            
            # Scale the background
            self.background = pygame.transform.scale(
                original_background, 
                (int(bg_width * scale_factor), int(bg_height * scale_factor))
            )
            
            print(f"Background scaled to {self.background.get_width()}x{self.background.get_height()}")
        except pygame.error:
            print("Could not load background image. Using default sky blue color.")
            self.background = pygame.Surface((2400, 1800))
            self.background.fill((135, 206, 235))

        # Physics constants
        self.GRAVITY = 0.8
        self.GROUND_LEVEL = 780  # Lower ground level for larger map

        # Game clock
        self.clock = pygame.time.Clock()
        self.fps = 60

        # Create player
        self.player = Player(300, 780)
        
        # Player Spawn Point
        self.spawn_point = (300, 780)

        # Create camera
        self.camera = Camera(self.screen_width, self.screen_height)

        # Create platforms across a larger map
        self.platforms = [
            Platform(0, self.GROUND_LEVEL , 4134, 200), # First Platform
            Platform(4265, self.GROUND_LEVEL, 890, 200), # Second Platform
            Platform(5345, self.GROUND_LEVEL, 3829, 200), # Third Platform
            Platform(9305, self.GROUND_LEVEL, 3323, 200), # Fourth Platform
        ]

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

        # Game state variables
        self.running = True
        
    def spawn_initial_monsters(self):
        """Spawn initial monsters in the level"""
        # Clear existing monsters
        self.monsters = []
        
        # Spawn all monsters from spawn points
        for monster_type, x, y in self.monster_spawn_points:
            monster = self.monster_spawner.spawn_monster(monster_type, x, y)
            self.monsters.append(monster)

    def handle_events(self):
        """Handle pygame events"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and not self.player.is_jumping:
                    self.player.jump()  
                elif event.key == pygame.K_ESCAPE and self.game_state == PLAYING:
                    self.game_state = PAUSED
            
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_SPACE:
                    self.player.release_jump()

        # Get pressed keys for movement
        keys = pygame.key.get_pressed()
        left = keys[pygame.K_LEFT] or keys[pygame.K_a]
        right = keys[pygame.K_RIGHT] or keys[pygame.K_d]
        
        # Use player's move method
        self.player.move(left, right)
        
    def player_die(self):
        """Handle player death"""
        if not self.player.is_death_animating:
            self.lives -= 1
            self.player.die()
            # Reset all monsters to their initial positions
            self.spawn_initial_monsters()
            
    def update(self):
        """Update game physics"""
        # Check for death first
        if self.player.rect.y > self.GROUND_LEVEL:
            self.player_die()
            
        # If death animation is playing, only update player
        if self.player.is_death_animating:
            self.player.update()
            # Check if player has fallen far enough to reset
            if self.player.rect.y > self.GROUND_LEVEL + 500:  # Wait until player falls well below screen
                if self.lives <= 0:
                    self.running = False
                else:
                    self.player.is_death_animating = False
                    self.player.is_dead = False
                    self.player.can_move = True
                    self.player.rect.x, self.player.rect.y = self.spawn_point
                    self.player.velocity_y = 0
                    self.player.velocity_x = 0
            return
        
        # First update monsters
        for monster in self.monsters:
            # Update monster position
            monster.update()
            
            # Apply platform collisions for monsters
            for platform in self.platforms:
                if monster.rect.colliderect(platform.rect):
                    # Landing on platform
                    if monster.velocity_y > 0:
                        monster.rect.bottom = platform.rect.top
                        monster.velocity_y = 0
                    # Hitting platform from below
                    elif monster.velocity_y < 0:
                        monster.rect.top = platform.rect.bottom
                        monster.velocity_y = 0
                    # Hitting platform from sides
                    elif monster.rect.right > platform.rect.left and monster.rect.left < platform.rect.left:
                        monster.rect.right = platform.rect.left
                        monster.velocity_x *= -1  # Reverse direction
                    elif monster.rect.left < platform.rect.right and monster.rect.right > platform.rect.right:
                        monster.rect.left = platform.rect.right
                        monster.velocity_x *= -1  # Reverse direction
            
            # Check collision with player
            if monster.rect.colliderect(self.player.rect):
                # Player is above monster (stomping)
                if (self.player.velocity_y > 0 and 
                    self.player.rect.bottom < monster.rect.centery + 10):
                    if isinstance(monster, Koopa) and monster.is_shell:
                        # Kick shell
                        direction = 1 if self.player.rect.centerx < monster.rect.centerx else -1
                        monster.kick_shell(direction)
                    else:
                        monster.die()
                        self.player.velocity_y = -10  # Bounce player up
                        self.score += 100
                elif monster.is_alive:  # Only die if monster is alive
                    # Player dies if touching monster from the side or below
                    self.player_die()
        
        # Remove dead Goombas that should be removed
        self.monsters = [monster for monster in self.monsters 
                        if not (isinstance(monster, Goomba) and monster.should_remove())]
            
        # Apply gravity
        self.player.velocity_y += self.GRAVITY
        self.player.rect.y += self.player.velocity_y

        # Check for platform collisions
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

        for block in self.blocks:
            if self.player.rect.colliderect(block.rect):
                # Check if the player is landing on the block
                if (
                    self.player.rect.top < block.rect.top
                    and self.player.velocity_y > 0
                    and self.player.rect.right > block.rect.left + 5  # Sufficient horizontal overlap (right side)
                    and self.player.rect.left < block.rect.right - 5  # Sufficient horizontal overlap (left side)
                ):
                    self.player.rect.bottom = block.rect.top
                    self.player.velocity_y = 0
                    self.player.is_jumping = False
                # Check if the player hits the bottom of the block
                elif (
                    self.player.rect.bottom > block.rect.bottom
                    and self.player.velocity_y < 0  # Moving upwards
                    and self.player.rect.right > block.rect.left + 5  # Avoid triggering on side collisions
                    and self.player.rect.left < block.rect.right - 5  # Avoid triggering on side collisions
                ):
                    self.player.rect.top = block.rect.bottom
                    self.player.velocity_y = self.GRAVITY  # Set a positive velocity to simulate falling
                    if isinstance(block, BlockInt):
                        block.hit()

                   
 
                # Check for left-side collision
                elif self.player.rect.right > block.rect.left and self.player.rect.left < block.rect.left:
                    self.player.rect.right = block.rect.left
                # Check for right-side collision
                elif self.player.rect.left < block.rect.right and self.player.rect.right > block.rect.right:
                    self.player.rect.left = block.rect.right

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
                    
        self.player.update()

        # Prevent falling through ground
        """ if self.player.rect.bottom > self.GROUND_LEVEL:
            self.player.rect.bottom = self.GROUND_LEVEL
            self.player.velocity_y = 0
            self.player.is_jumping = False """
            
        # Prevent moving off screen
        if self.player.rect.left < 0:
            self.player.rect.left = 0

        # Update camera to follow player
        self.camera.update(self.player)
        
    def draw(self):
        """Draw game objects"""
        self.screen.fill((0, 0, 0))

        # Draw background with camera offset
        self.screen.blit(self.background, self.camera.camera)

        # Draw platforms
        for platform in self.platforms:
            if self.camera.camera.colliderect(platform.rect):
                pygame.draw.rect(self.screen, (139, 69, 19), self.camera.apply_rect(platform.rect))
        
        for tube in self.tubes:
            tube.draw(self.screen, self.camera)

        for block in self.blocks:
            block.draw(self.screen, self.camera)
        
        for monster in self.monsters:
            monster.draw(self.screen, self.camera)

        # Draw player
        self.player.draw(self.screen, self.camera)
        
        # Draw UI elements
        score_text = self.font.render(f'Score: {self.score}', True, (255, 255, 255))
        lives_text = self.font.render(f'Lives: {self.lives}', True, (255, 255, 255))
        
        self.screen.blit(score_text, (10, 10))
        self.screen.blit(lives_text, (10, 50))

        pygame.display.flip()

    def run(self):
        """Main game loop"""
        while self.running:
            if self.game_state == MENU:
                self.game_state = self.menu.handle_input()
                self.menu.draw(self.screen)
                
                if self.game_state == QUIT:
                    self.running = False
            elif self.game_state == PLAYING:
                self.handle_events()
                self.update()
                self.draw()
            elif self.game_state == PAUSED:
                self.game_state = self.pause_menu.handle_input()
                self.draw()
                self.pause_menu.draw(self.screen)
                if self.game_state == RESTART:
                    self.__init__()
                    self.game_state = PLAYING
                elif self.game_state == QUIT_TO_MAIN_MENU:
                    self.game_state = MENU
        
            pygame.display.flip()
            self.clock.tick(self.fps)