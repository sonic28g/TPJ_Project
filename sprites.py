import pygame
from Player import Player
from Spritesheet import SpriteSheet

CELL_SIZE = 16

class MarioSprite(pygame.sprite.Sprite):
    def __init__(self, player: Player, WIDTH, HEIGHT, SCALE):
        super().__init__()

        MARIO_SPRITESHEET = SpriteSheet("img/mario_sprites.png")

        self.player = player
        self.SCALE = SCALE

        mario_map = {
            "death": (6, 1, CELL_SIZE, CELL_SIZE),
            "small_stand": (0, 1, CELL_SIZE, CELL_SIZE),
            "small_run_1": (1, 1, CELL_SIZE, CELL_SIZE),
            "small_run_2": (2, 1, CELL_SIZE, CELL_SIZE),
            "small_run_3": (3, 1, CELL_SIZE, CELL_SIZE),
            "small_turn": (4, 1, CELL_SIZE, CELL_SIZE),
            "small_jump": (5, 1, CELL_SIZE, CELL_SIZE),
            "medium": (12, 0, CELL_SIZE, CELL_SIZE * 2),
            "big_stand": (13, 0, CELL_SIZE, CELL_SIZE * 2),
            "big_run_1": (14, 0, CELL_SIZE, CELL_SIZE * 2),
            "big_run_2": (15, 0, CELL_SIZE, CELL_SIZE * 2),
            "big_run_3": (16, 0, CELL_SIZE, CELL_SIZE * 2),
            "big_turn": (17, 0, CELL_SIZE, CELL_SIZE * 2),
            "big_jump": (18, 0, CELL_SIZE, CELL_SIZE * 2),
            "big_crouch": (19, 0, CELL_SIZE, CELL_SIZE * 2),
            "fire_stand": (26, 0, CELL_SIZE, CELL_SIZE * 2),
            "fire_lanch": (27, 0, CELL_SIZE, CELL_SIZE * 2),
            "big_run_1": (28, 0, CELL_SIZE, CELL_SIZE * 2),
            "big_run_2": (29, 0, CELL_SIZE, CELL_SIZE * 2),
            "big_run_3": (30, 0, CELL_SIZE, CELL_SIZE * 2),
            "big_turn": (31, 0, CELL_SIZE, CELL_SIZE * 2),
            "big_jump": (32, 0, CELL_SIZE, CELL_SIZE * 2),
            "big_crouch": (33, 0, CELL_SIZE, CELL_SIZE * 2),
        }

        self.mario_images = {
            name: pygame.transform.scale(
                MARIO_SPRITESHEET.image_at(
                    (a * CELL_SIZE, b * CELL_SIZE, sa, sb), -1),(SCALE, SCALE),)
            for (name, (a, b, sa, sb)) in mario_map.items()
        }

        self.image = pygame.Surface([WIDTH * SCALE, HEIGHT * SCALE])
        self.update("small_stand")
        self.rect = self.image.get_rect()

    def update(self, frame):
        self.image.fill("white")
        self.image.set_colorkey("white")

        # Rander
        self.image.blit(
            self.mario_images[frame],
            (self.SCALE * self.mario.pos[0], self.SCALE * self.mario.pos[1]),
        )
