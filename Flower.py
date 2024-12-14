import pygame as pg

class Flower(pg.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.sprites = []
        for i in range(4):
            sprite = pg.image.load(f'assets/items/flower{i}.png').convert_alpha()
            self.sprites.append(pg.transform.scale(sprite, (48, 48)))
        
        self.current_sprite = 0
        self.animation_speed = 0.15
        self.image = self.sprites[self.current_sprite]
        self.rect = self.image.get_rect()
        self.rect.centerx = x + 30
        self.rect.bottom = y + 30
        
        self.is_emerging = True
        self.is_active = False
        self.emergence_height = 0

    def update(self):
        if self.is_active:
            if self.is_emerging:
                if self.emergence_height < 30:
                    self.rect.y -= 2
                    self.emergence_height += 2
                else:
                    self.is_emerging = False
            
            self.current_sprite += self.animation_speed
            if self.current_sprite >= len(self.sprites):
                self.current_sprite = 0
            self.image = self.sprites[int(self.current_sprite)]

    def draw(self, screen, camera):
        if self.is_active:
            screen.blit(self.image, camera.apply(self))

    def activate(self):
        self.is_active = True