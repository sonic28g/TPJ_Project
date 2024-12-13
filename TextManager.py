import pygame

class TextManager:
    def __init__(self, font_path=None, font_size=36):
        self.font = pygame.font.Font(font_path, font_size)

    def render_text(self, text, color=(255, 255, 255)):
        return self.font.render(text, True, color)
