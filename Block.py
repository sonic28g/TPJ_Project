import pygame as pg
from Settings import GROUND_LEVEL
from Powerup import Mushroom, Flower
from Coin import Coin

class Block(pg.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.rect = pg.Rect(x, y, 64, 60)

    def draw(self, screen, camera):
        screen.blit(self.image, camera.apply(self))

class BlockBreak(Block):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.image = pg.image.load('assets/level/tiles.png').convert_alpha()
        self.image = self.image.subsurface(32*2,0,32,32)
        self.image = pg.transform.scale(self.image, (60, 60))
        self.original_y = y
        self.is_animating = False
        self.animation_progress = 0
        self.animation_speed = 2
        self.max_offset = 15
        self.is_broken = False
        self.debris_list = []
        self.active = True

    def update(self):
        # Update debris first
        for debris in self.debris_list[:]:
            debris.update()
            if debris.rect.y > GROUND_LEVEL:
                self.debris_list.remove(debris)

        # Then update block animation
        if self.is_animating and not self.is_broken:
            if self.animation_progress < self.max_offset:
                self.rect.y = self.original_y - self.animation_progress
                self.animation_progress += self.animation_speed
            elif self.animation_progress < self.max_offset * 2:
                self.rect.y = self.original_y - (self.max_offset * 2 - self.animation_progress)
                self.animation_progress += self.animation_speed
            else:
                self.rect.y = self.original_y
                self.is_animating = False
                self.animation_progress = 0

    def create_debris(self):
        directions = [(-1, 1), (1, 1), (-1, 0.5), (1, 0.5)]
        for dx, dy in directions:
            debris = BlockDebris(self.rect.centerx, self.rect.centery, dx, dy)
            self.debris_list.append(debris)

    def hit(self, is_big):
        if not self.is_animating and not self.is_broken and self.active:
            self.is_animating = True
            if is_big:
                self.is_broken = True
                self.active = False
                self.create_debris()

    def reset(self):
        self.is_broken = False
        self.is_animating = False
        self.animation_progress = 0
        self.debris_list.clear()
        self.rect.y = self.original_y

    def draw(self, screen, camera):
        if not self.is_broken:
            screen.blit(self.image, camera.apply(self))
        for debris in self.debris_list:
            debris.draw(screen, camera)

class BlockDebris(pg.sprite.Sprite):
    def __init__(self, x, y, direction_x, direction_y):
        super().__init__()
        self.original_image = pg.image.load('assets/level/block_debris.png').convert_alpha()
        self.original_image = pg.transform.scale(self.original_image, (30, 30))
        self.image = self.original_image
        self.rect = self.image.get_rect(center=(x, y))
        self.velocity_x = direction_x * 5
        self.velocity_y = direction_y * -10
        self.gravity = 0.5
        self.rotation = 0
        self.rotation_speed = direction_x * 5

    def update(self):
        self.velocity_y += self.gravity
        self.rect.x += self.velocity_x
        self.rect.y += self.velocity_y
        self.rotation += self.rotation_speed
        self.image = pg.transform.rotate(self.original_image, self.rotation)
        self.rect = self.image.get_rect(center=self.rect.center)

    def draw(self, screen, camera):
        screen.blit(self.image, camera.apply(self))

class BlockInt(Block):
    def __init__(self, x, y, content=None):
        super().__init__(x, y)
        self.tiles = pg.image.load('assets/level/tiles.png').convert_alpha()
        self.frames = [
            pg.transform.scale(self.tiles.subsurface(32*3, 0, 32, 32), (60, 60)),
            pg.transform.scale(self.tiles.subsurface(32*4, 0, 32, 32), (60, 60)),
            pg.transform.scale(self.tiles.subsurface(32*5, 0, 32, 32), (60, 60))
        ]
        self.frame_index = 0
        self.animation_speed = 0.2
        self.animation_timer = 0
        self.image = self.frames[0]
        self.has_been_hit = False
        self.original_y = y
        self.is_animating = False
        self.animation_progress = 0
        self.move_speed = 2
        self.max_offset = 15
        self.mushroom = None
        self.coin = None
        self.flower = None
        self.content = content

    def update(self):
        if not self.has_been_hit:
            self.animation_timer += self.animation_speed
            if self.animation_timer >= 1:
                self.animation_timer = 0
                self.frame_index = (self.frame_index + 1) % len(self.frames)
                self.image = self.frames[self.frame_index]

        if self.is_animating:
            if self.animation_progress < self.max_offset:
                self.rect.y = self.original_y - self.animation_progress
                self.animation_progress += self.move_speed
            elif self.animation_progress < self.max_offset * 2:
                self.rect.y = self.original_y - (self.max_offset * 2 - self.animation_progress)
                self.animation_progress += self.move_speed
            else:
                self.rect.y = self.original_y
                self.is_animating = False
                self.animation_progress = 0

    def hit(self, is_big=False):
        if not self.has_been_hit:
            self.has_been_hit = True
            self.is_animating = True
            if self.content == 'mushroom' and not self.mushroom:
                self.mushroom = Mushroom(self.rect.x, self.rect.y)
                self.mushroom.activate()
            elif self.content == 'flower' and not self.flower:
                self.flower = Flower(self.rect.x, self.rect.y)
                self.flower.activate()
            elif self.content == 'coin':
                self.coin = Coin(self.rect.x, self.rect.y)
            self.image = pg.image.load('assets/level/tiles.png').convert_alpha()
            self.image = self.image.subsurface(32*6, 0, 32, 32)
            self.image = pg.transform.scale(self.image, (60, 60))

    def reset(self):
        self.has_been_hit = False
        self.is_animating = False
        self.animation_progress = 0
        self.rect.y = self.original_y
        self.frame_index = 0
        self.animation_timer = 0
        self.image = self.frames[0]
        self.flower = None  # Reset flower
        self.mushroom = None  # Reset mushroom
        self.coin = None  # Reset coin

class BlockBrick(Block):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.image = pg.image.load('assets/level/tiles.png').convert_alpha()
        self.image = self.image.subsurface(32*1,0,32,32)
        self.image = pg.transform.scale(self.image, (60, 60))
