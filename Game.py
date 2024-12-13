import pygame
from Camera import Camera
from Player import Player
from MainMenu import MainMenu
from PauseMenu import PauseMenu
from MonsterSpawner import MonsterSpawner
from Settings import *
from Block import *
from World import World

class Game:
    def __init__(self):
        # Initialize Pygame
        pygame.init()
        pygame.font.init()
        pygame.mixer.init()
        
        # UI font
        self.font = pygame.font.Font(None, 36)

        # Screen setup
        self.screen_width = SCREEN_WIDTH
        self.screen_height = SCREEN_HEIGHT
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        pygame.display.set_caption(GAME_TITLE)
        
        # Game state variables
        self.running = True
        self.game_state = MENU
        
        # Menus
        self.menu = MainMenu(self.screen_width, self.screen_height)
        self.pause_menu = PauseMenu(self.screen_width, self.screen_height)

        # Game clock
        self.clock = pygame.time.Clock()
        self.fps = 60

        # Player
        self.player = Player(300, 780)
        
        # World
        self.world = World()
        
        # Camera
        self.camera = Camera(self.screen_width, self.screen_height)
        

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
            
    def update(self):
        """Update game physics"""
        # Check for death first
        if self.player.rect.y > GROUND_LEVEL:
            self.world.player_die(self.player)
            
        # If death animation is playing, only update player
        if self.player.is_death_animating:
            self.player.update()
            # Check if player has fallen far enough to reset
            if self.player.rect.y > GROUND_LEVEL + 500:  # Wait until player falls well below screen
                if self.world.lives <= 0:
                    self.running = False
                else:
                    self.player.is_death_animating = False
                    self.player.is_dead = False
                    self.player.can_move = True
                    self.player.rect.x, self.player.rect.y = self.world.spawn_point
                    self.player.velocity_y = 0
                    self.player.velocity_x = 0
            return
        
        self.world.update(self.player)
        self.player.update()
            
        # Prevent player moving off screen
        if self.player.rect.left < 0:
            self.player.rect.left = 0
            
        # Update camera to follow player
        self.camera.update(self.player)
        
    def draw(self):
        """Draw game objects"""
        self.screen.fill((0, 0, 0))

        # Draw world
        self.world.draw(self.screen, self.camera)

        # Draw player
        self.player.draw(self.screen, self.camera)
        
        # Draw UI elements
        score_text = self.font.render(f'Score: {self.world.score}', True, (255, 255, 255))
        lives_text = self.font.render(f'Lives: {self.world.lives}', True, (255, 255, 255))
        
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