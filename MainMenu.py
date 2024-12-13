import pygame
from Settings import *

class MainMenu:
    def __init__(self, screen_width, screen_height):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.menu_options = ["Start Game", "Quit"]
        self.selected_option = 0
        self.font = pygame.font.Font('./assets/fonts/emulogic.ttf', 36)

    def handle_input(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return QUIT
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    self.selected_option = (self.selected_option - 1) % len(self.menu_options)
                elif event.key == pygame.K_DOWN:
                    self.selected_option = (self.selected_option + 1) % len(self.menu_options)
                elif event.key == pygame.K_RETURN:
                    if self.menu_options[self.selected_option] == "Start Game":
                        return PLAYING
                    elif self.menu_options[self.selected_option] == "Quit":
                        return QUIT
        return MENU

    def draw(self, screen):
        screen.fill((0, 0, 0))
        title = self.font.render("Super Mario Remake", True, (255, 255, 255))
        title_rect = title.get_rect(center=(self.screen_width // 2, 200))
        screen.blit(title, title_rect)

        for i, option in enumerate(self.menu_options):
            color = (255, 255, 0) if i == self.selected_option else (255, 255, 255)
            text = self.font.render(option, True, color)
            text_rect = text.get_rect(center=(self.screen_width // 2, 300 + i * 50))
            screen.blit(text, text_rect)