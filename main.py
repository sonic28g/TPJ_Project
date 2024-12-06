import pygame
import sys
import os
from Camera import Camera
from Player import Player
from Platform import Platform
from Settings import *

class SuperMario:
    def __init__(self):
        # Initialize Pygame
        pygame.init()

        # Screen setup
        self.screen_width = 900
        self.screen_height = 600
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        pygame.display.set_caption("Super Mario Remake")

        # Load and scale background image properly
        try:
            # Load original background
            background_path = os.path.join('assets', 'level.png')
            original_background = pygame.image.load(background_path).convert()
            
            # Calculate scaling to maintain aspect ratio
            bg_width = original_background.get_width()
            bg_height = original_background.get_height()
            
            # Determine scale factor to match game world size
            scale_factor = max(2400 / bg_width, 1800 / bg_height)
            
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

        # Create camera
        self.camera = Camera(self.screen_width, self.screen_height)

        # Create platforms across a larger map
        self.platforms = [
            Platform(0, self.GROUND_LEVEL, 2400, 200),  # Ground platform
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

        # Get pressed keys for movement
        keys = pygame.key.get_pressed()
        left = keys[pygame.K_LEFT] or keys[pygame.K_a]
        right = keys[pygame.K_RIGHT] or keys[pygame.K_d]
        
        # Use player's move method
        self.player.move(left, right)

    def update(self):
        """Update game physics"""
        # Apply gravity
        self.player.velocity_y += self.GRAVITY
        self.player.rect.y += self.player.velocity_y

        # Check for platform collisions
        for platform in self.platforms:
            if self.player.rect.colliderect(platform.rect):
                # If falling onto platform
                if self.player.velocity_y > 0:
                    self.player.rect.bottom = platform.rect.top
                    self.player.velocity_y = 0
                    self.player.is_jumping = False
                # If jumping into platform from underneath
                elif self.player.velocity_y < 0:
                    self.player.rect.top = platform.rect.bottom
                    self.player.velocity_y = 0
                    
        self.player.update()

        # Prevent falling through ground
        if self.player.rect.bottom > self.GROUND_LEVEL:
            self.player.rect.bottom = self.GROUND_LEVEL
            self.player.velocity_y = 0
            self.player.is_jumping = False
            
        # Prevent moving off screen
        if self.player.rect.left < 0:
            self.player.rect.left = 0

        # Update camera to follow player
        self.camera.update(self.player)

    def draw(self):
        """Draw game objects"""
        # Clear the screen
        self.screen.fill((0, 0, 0))

        # Draw background with camera offset
        self.screen.blit(self.background, self.camera.camera)

        # Draw platforms
        for platform in self.platforms:
            # Only draw platforms that are within the camera view
            if self.camera.camera.colliderect(platform.rect):
                pygame.draw.rect(self.screen, platform.color, 
                                 self.camera.apply_rect(platform.rect))

        # Draw player
        # pygame.draw.rect(self.screen, self.player.color, self.camera.apply(self.player))
        self.player.draw(self.screen, self.camera)
        
        # Update display
        pygame.display.flip()

    def run(self):
        """Main game loop"""
        while self.running:
            # Handle events
            self.handle_events()

            # Update game state
            self.update()

            # Draw game objects
            self.draw()

            # Control game speed
            self.clock.tick(self.fps)

        # Quit the game
        pygame.quit()
        sys.exit()

def main():
    """Initialize and run the game"""
    game = SuperMario()
    game.run()

if __name__ == "__main__":
    main()