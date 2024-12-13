import pygame

class UIManager:
    def __init__(self, screen, font_manager):
        self.screen = screen
        self.font_manager = font_manager
        self.elements = []

    def add_text(self, text, position, color=(255, 255, 255)):
        rendered_text = self.font_manager.render_text(text, color)
        self.elements.append((rendered_text, position))

    def clear(self):
        self.elements = []

    def draw(self):
        for element, position in self.elements:
            self.screen.blit(element, position)