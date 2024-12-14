import pygame as pg
from Settings import GRAVITY

class Coin(pg.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.frames = []
        for i in range(4):
            image = pg.image.load(f'assets/items/coin_{i}.png').convert_alpha()
            image = pg.transform.scale(image, (32, 32))
            self.frames.append(image)
        
        self.frame_index = 0
        self.animation_speed = 0.1
        self.velocity_y = -15
        self.is_collected = False
        self.original_y = y
        
        self.image = self.frames[0]
        self.rect = self.image.get_rect()
        # Center the coin relative to the block position
        self.rect.centerx = x + 30  # Half of block width (60/2)
        self.rect.centery = y + 30  # Half of block height (60/2)
            
    def update(self):
        self.frame_index += self.animation_speed
        if self.frame_index >= len(self.frames):
            self.frame_index = 0
        self.image = self.frames[int(self.frame_index)]
        
        self.velocity_y += GRAVITY
        self.rect.y += self.velocity_y
        
        if self.velocity_y > 0 and self.rect.y > self.original_y - 48:
            self.is_collected = True
            
    def draw(self, screen, camera):
        screen_pos = camera.apply(self)
        screen.blit(self.image, screen_pos)