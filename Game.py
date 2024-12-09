import pygame
import sys
import os
from Tube import Tube
from camera import Camera
from Player import Player
from Platform import Platform
from MainMenu import MainMenu
from PauseMenu import PauseMenu
from Settings import *
from Settings import *

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
        self.screen_width = 900
        self.screen_height = 600
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        pygame.display.set_caption(GAME_TITLE)
        
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
            Tube(1600,700),
        ]

        # Game state variables
        self.running = True

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

        # Get pressed keys for movement
        keys = pygame.key.get_pressed()
        left = keys[pygame.K_LEFT] or keys[pygame.K_a]
        right = keys[pygame.K_RIGHT] or keys[pygame.K_d]
        
        # Use player's move method
        self.player.move(left, right)
        
    def player_die(self):
        """Handle player death"""
        self.lives -= 1
        if self.lives <= 0:
            self.running = False
        self.player.rect.x, self.player.rect.y = self.spawn_point
        self.player.velocity_y = 0
        self.player.velocity_x = 0

    def update(self):
        """Update game physics"""
        # Apply gravity
        self.player.velocity_y += self.GRAVITY
        self.player.rect.y += self.player.velocity_y

        # Check for platform collisions
        for platform in self.platforms:
            if self.player.rect.colliderect(platform.rect):
                if self.player.velocity_y > 0:
                    self.player.rect.bottom = platform.rect.top
                    self.player.velocity_y = 0
                    self.player.is_jumping = False
                elif self.player.velocity_y < 0:
                    self.player.rect.top = platform.rect.bottom
                    self.player.velocity_y = 0

        for tube in self.tubes:
            if tube.rect.colliderect(self.player.rect):
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
                    # Collision from the left
                    self.player.rect.right = tube.rect.left

                elif self.player.rect.left < tube.rect.right and self.player.rect.right > tube.rect.right:
                    # Collision from the right
                    self.player.rect.left = tube.rect.right
                    
        self.player.update()

        # Prevent falling through ground
        """ if self.player.rect.bottom > self.GROUND_LEVEL:
            self.player.rect.bottom = self.GROUND_LEVEL
            self.player.velocity_y = 0
            self.player.is_jumping = False """
            
        # Check for death
        if self.player.rect.y > self.GROUND_LEVEL:
            self.player_die()
            
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

        print(self.player.rect)

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