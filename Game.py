import pygame
from Settings import *
from MainMenu import MainMenu
from PauseMenu import PauseMenu
from World import World
from Camera import Camera
from Command import *

class Game:
    def __init__(self):
        # Initialize Pygame
        pygame.init()
        pygame.font.init()
        pygame.mixer.init()

        # Screen setup
        self.screen_width = SCREEN_WIDTH
        self.screen_height = SCREEN_HEIGHT
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        pygame.display.set_caption(GAME_TITLE)
        
        # Input handler setup
        self.input_handler = InputHandler()
        
        # Game state variables
        self.running = True
        self.game_state = MENU
        
        # Singleton Camera
        self.camera = Camera.getInstance(self.screen_width, self.screen_height)
        
        # Menus
        self.menu = MainMenu(self.screen_width, self.screen_height)
        self.pause_menu = PauseMenu(self.screen_width, self.screen_height)

        # Game clock
        self.clock = pygame.time.Clock()
        self.fps = 60
        
        # World
        self.world = World(self.screen, self.camera)
        
    def handle_events(self):
        """Handle pygame events"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            
            if event.type == pygame.KEYDOWN:
                self.input_handler.handle_keydown(event, self.world.player)
                if event.key == pygame.K_ESCAPE and self.game_state == PLAYING:
                    self.game_state = PAUSED
            
            if event.type == pygame.KEYUP:
                self.input_handler.handle_keyup(event, self.world.player)

        # Handle continuous input (movement)
        if self.game_state == PLAYING:
            self.input_handler.handle_continuous_input(self.world.player)
            
    def update(self):
        """Update game"""
        
        # Update world (player within)
        self.world.update()
        
        if self.world.is_gameover:
            self.game_state = MENU
            self.world = World(self.screen)
        
    def draw(self):
        """Draw game objects"""
        self.screen.fill((0, 0, 0))

        # Draw world (player within)
        self.world.draw(self.screen)

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
                if self.game_state == QUIT:
                    self.running = False
                self.draw()
                self.pause_menu.draw(self.screen)
                if self.game_state == RESTART:
                    self.__init__()
                    self.game_state = PLAYING
                elif self.game_state == QUIT_TO_MAIN_MENU:
                    self.game_state = MENU
        
            pygame.display.flip()
            self.clock.tick(self.fps)