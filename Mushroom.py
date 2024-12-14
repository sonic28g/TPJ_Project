import pygame
from Settings import GRAVITY

class Mushroom(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.image.load('assets/items/mushroom.png').convert_alpha()
        self.image = pygame.transform.scale(self.image, (48, 48))
        self.rect = self.image.get_rect()
        self.rect.centerx = x + 30
        self.rect.centery = y + 30
        self.velocity_x = 3
        self.velocity_y = 0
        self.is_active = False
        self.is_emerging = True
        self.emergence_height = 0
        
    def update(self):
        if self.is_active:
            if self.is_emerging:
                if self.emergence_height < 48:
                    self.rect.y -= 2
                    self.emergence_height += 2
                else:
                    self.is_emerging = False
            else:
                self.velocity_y += GRAVITY
                self.rect.x += self.velocity_x
                self.rect.y += self.velocity_y
            
    def draw(self, screen, camera):
        if self.is_active:
            screen.blit(self.image, camera.apply(self))

    def activate(self):
        self.is_active = True
        self.velocity_y = -10