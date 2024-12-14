import pygame

class Pole(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.image.load('assets/level/pole.png').convert_alpha()
        self.image = pygame.transform.scale(self.image, (32, 570))
        self.rect = self.image.get_rect(bottomleft=(x, y))
        
    def draw(self, screen, camera):
        screen.blit(self.image, camera.apply(self))
        
class Flag(pygame.sprite.Sprite):
    def __init__(self, pole):
        super().__init__()
        self.image = pygame.image.load('assets/level/flag.png').convert_alpha()
        self.image = pygame.transform.scale(self.image, (64, 64))
        self.pole = pole
        # Adjust x position to align with pole
        flag_x = pole.rect.x - self.image.get_width() + 76
        flag_y = pole.rect.y + 32
        self.rect = self.image.get_rect(topright=(flag_x, flag_y))
        self.is_sliding = False
        self.slide_speed = 3
        
    def update(self):
        if self.is_sliding:
            if self.rect.bottom < self.pole.rect.bottom - 32:
                self.rect.y += self.slide_speed
            else:
                self.is_sliding = False
                # Signal to World that flag reached bottom
                return True
        return False

    def start_slide(self):
        if not self.is_sliding:
            self.is_sliding = True
        
    def draw(self, screen, camera):
        screen.blit(self.image, camera.apply(self))