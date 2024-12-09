import pygame
from Settings import *

class PauseMenu:
    def __init__(self, screen_width, screen_height):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.menu_options = ["Resume", "Restart", "Quit to Main Menu"]
        self.selected_option = 0
        self.font = pygame.font.Font(None, 36)
        self.overlay = pygame.Surface((screen_width, screen_height))
        self.overlay.fill((0, 0, 0))
        self.overlay.set_alpha(128)

    def handle_input(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return QUIT
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return PLAYING
                if event.key == pygame.K_UP:
                    self.selected_option = (self.selected_option - 1) % len(self.menu_options)
                elif event.key == pygame.K_DOWN:
                    self.selected_option = (self.selected_option + 1) % len(self.menu_options)
                elif event.key == pygame.K_RETURN:
                    if self.menu_options[self.selected_option] == "Resume":
                        return PLAYING
                    elif self.menu_options[self.selected_option] == "Restart":
                        return RESTART
                    elif self.menu_options[self.selected_option] == "Quit to Main Menu":
                        return MENU
        return PAUSED

    def draw(self, screen):
        # Draw semi-transparent overlay
        screen.blit(self.overlay, (0, 0))
        
        # Draw menu title
        title = self.font.render("PAUSED", True, (255, 255, 255))
        title_rect = title.get_rect(center=(self.screen_width // 2, 200))
        screen.blit(title, title_rect)

        # Draw menu options
        for i, option in enumerate(self.menu_options):
            color = (255, 255, 0) if i == self.selected_option else (255, 255, 255)
            text = self.font.render(option, True, color)
            text_rect = text.get_rect(center=(self.screen_width // 2, 300 + i * 50))
            screen.blit(text, text_rect)