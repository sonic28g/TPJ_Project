import pygame
import os
from Platform import Platform
from Tube import Tube
from Block import BlockInt, BlockBreak, BlockBrick
from MonsterSpawner import MonsterSpawner
from Settings import *
from Koopa import Koopa
from Goomba import Goomba
from Player import Player
from Camera import Camera
from TextManager import TextManager
from UIManager import UIManager
from Pole import Pole, Flag
from Powerup import Mushroom, Flower
from CollisionSystem import CollisionSystem, PowerUpCollisionHandler, PlayerCollisionHandler, EnemyCollisionHandler

class World:
    def __init__(self, screen):
        # Load background
        self.background = self.load_background()
        
        # Stats
        self.score = 0
        self.lives = 3
        self.coins = 0
        self.time = 400
        self.timer = pygame.time.get_ticks()
        
        # Game Over
        self.is_gameover = False
        
        # Level Complete
        self.level_complete = False
        
        # Text and UI Managers
        self.TextManager = TextManager('./assets/fonts/emulogic.ttf', 28)
        self.UIManager = UIManager(screen, self.TextManager)
        
        # Initialize collision system
        self.collision_system = CollisionSystem()
        self.collision_system.add_observer(PowerUpCollisionHandler(self))
        self.collision_system.add_observer(PlayerCollisionHandler(self))
        self.collision_system.add_observer(EnemyCollisionHandler(self))
        
        # Player
        self.player = Player(300, 780)
        self.spawn_point = (300, 780)
        
        # Camera
        self.camera = Camera(SCREEN_WIDTH, SCREEN_HEIGHT)
        
        # World elements
        self.platforms = [
            Platform(0, GROUND_LEVEL , 4134, 200), # First Platform
            Platform(4265, GROUND_LEVEL, 890, 200), # Second Platform
            Platform(5345, GROUND_LEVEL, 3829, 200), # Third Platform
            Platform(9305, GROUND_LEVEL, 3323, 200), # Fourth Platform
        ]
        
        self.tubes = [
            Tube(1676,660),
            Tube(2276,600),
            Tube(2756,540),
            Tube(3416,540),
            Tube(9776,660),
            Tube(10736,660),
        ]

        self.blocks = [
            BlockInt(960,540, content='mushroom'),
            BlockBreak(1200,540),
            BlockInt(1260,540, content='coin'),
            BlockBreak(1320,540),
            BlockInt(1380,540, content='coin'),
            BlockBreak(1440,540),
            BlockInt(1320,300, content='coin'),
            BlockBreak(4620,540),
            BlockInt(4680,540, content='coin'),
            BlockBreak(4740,540),
            BlockBreak(4800,300),
            BlockBreak(4860,300),
            BlockBreak(4920,300),
            BlockBreak(4980,300),
            BlockBreak(5040,300),
            BlockBreak(5100,300),
            BlockBreak(5160,300),
            BlockBreak(5220,300),
            BlockBreak(5460,300),
            BlockBreak(5520,300),
            BlockBreak(5580,300),
            BlockInt(5640,300, content='coin'),
            BlockBreak(5640,540),
            BlockBreak(6000,540),
            BlockBreak(6060,540),
            BlockInt(6360,540, content='mushroom'),
            BlockInt(6540,540, content='coin'),
            BlockInt(6540,300, content='coin'),
            BlockInt(6720,540, content='coin'),
            BlockBreak(7080,540),
            BlockBreak(7260,300),
            BlockBreak(7320,300),
            BlockBreak(7380,300),
            BlockBreak(7680,300),
            BlockInt(7740,300, content='coin'),
            BlockInt(7800,300, content='coin'),
            BlockBreak(7860,300),
            BlockBreak(7740,540),
            BlockBreak(7800,540),
            BlockBrick(8040,720),
            BlockBrick(8100,660),
            BlockBrick(8160,600),
            BlockBrick(8220,540),
            BlockBrick(8220,600),
            BlockBrick(8220,660),
            BlockBrick(8220,720),
            BlockBrick(8400,540),
            BlockBrick(8400,600),
            BlockBrick(8400,660),
            BlockBrick(8400,720),
            BlockBrick(8460,600),
            BlockBrick(8520,660),
            BlockBrick(8580,720),
            BlockBrick(8880,720),
            BlockBrick(8940,660),
            BlockBrick(9000,600),
            BlockBrick(9060,540),
            BlockBrick(9120,540),
            BlockBrick(9120,600),
            BlockBrick(9120,660),
            BlockBrick(9120,720),
            BlockBrick(9300,540),
            BlockBrick(9300,600),
            BlockBrick(9300,660),
            BlockBrick(9300,720),
            BlockBrick(9360,600),
            BlockBrick(9420,660),
            BlockBrick(9480,720),
            BlockBreak(10080,540),
            BlockBreak(10140,540),
            BlockInt(10200,540, content='mushroom'),
            BlockBreak(10260, 540),
            BlockBrick(10860,720),
            BlockBrick(10920,660),
            BlockBrick(10980,600),
            BlockBrick(11040,540),
            BlockBrick(11100,480),
            BlockBrick(11160,420),
            BlockBrick(11220,360),
            BlockBrick(11280,300),
            BlockBrick(11340,300),
            BlockBrick(11340,360),
            BlockBrick(11340,420),
            BlockBrick(11340,480),
            BlockBrick(11340,540),
            BlockBrick(11340,600),
            BlockBrick(11340,660),
            BlockBrick(11340,720),
            BlockBrick(11880, 720),
        ]
                
        # Monster System
        self.monster_spawner = MonsterSpawner()
        self.monsters = []
        self.monster_spawn_points = [
            ('goomba', 1500, GROUND_LEVEL),
            ('koopa', 2500, GROUND_LEVEL),
            ('goomba', 5500, GROUND_LEVEL),
        ]
        
        self.spawn_initial_entities()
        
        # Victory flag
        self.pole = Pole(11891, 720)
        self.flag = Flag(self.pole)

    def load_background(self):
        try:
            bg_path = os.path.join('assets', 'level/level.png')
            original_bg = pygame.image.load(bg_path).convert()
            scale_factor = max(2400 / original_bg.get_width(), 1800 / original_bg.get_height())
            return pygame.transform.scale(original_bg, (
                int(original_bg.get_width() * scale_factor),
                int(original_bg.get_height() * scale_factor)
            ))
        except pygame.error:
            bg = pygame.Surface((2400, 1800))
            bg.fill((135, 206, 235))
            return bg

    def player_die(self):
        """Handle player death"""
        if not self.player.is_death_animating and not self.player.is_leveling_up:
            self.lives -= 1
            self.player.die()
            self.spawn_initial_entities()
    
    def spawn_initial_entities(self):
        self.monsters = []
        for monster_type, x, y in self.monster_spawn_points:
            monster = self.monster_spawner.spawn_monster(monster_type, x, y)
            self.monsters.append(monster)
        # Reset blocks
        for block in self.blocks:
            if isinstance(block, (BlockBreak, BlockInt)):
                block.reset()

    def update(self):
        # Keep time tracking
        current_time = pygame.time.get_ticks()
        if current_time - self.timer >= 1000:  
            self.time -= 1
            self.timer = current_time
            if self.time <= 0:
                self.player_die()
        
        # Check for death first
        if self.player.rect.y > GROUND_LEVEL:
            self.player_die()
            
        # If death animation is playing, only update player
        if self.player.is_death_animating:
            self.player.update()
            # Check if player has fallen far enough to reset
            if self.player.rect.y > GROUND_LEVEL + 1500:  
                if self.lives <= 0:
                    self.is_gameover = True
                else:
                    self.player.is_death_animating = False
                    self.player.is_dead = False
                    self.player.can_move = True
                    self.player.rect.x, self.player.rect.y = self.spawn_point
                    self.player.velocity_y = 0
                    self.player.velocity_x = 0
            return

        # Apply gravity to player
        self.player.velocity_y += GRAVITY
        self.player.rect.y += self.player.velocity_y
        
        # Use collision system to handle collisions
        self.collision_system.check_collisions(self)
        
        # Update player
        self.player.update()

        # Update monsters
        active_monsters = []
        for monster in self.monsters:
            monster.update()
            if monster.is_alive or isinstance(monster, Koopa) or (isinstance(monster, Goomba) and not monster.should_remove()):
                active_monsters.append(monster)
        self.monsters = active_monsters

        # Update blocks
        for block in self.blocks:
            block.update()
            # Handle coin collection from blocks
            if isinstance(block, BlockInt) and block.coin:
                block.coin.update()
                if block.coin.is_collected:
                    self.coins += 1
                    self.score += 200
                    block.coin = None
                    
                    
        # Update flag
        self.flag.update()
        if self.player.is_sliding and not self.flag.is_sliding:
            self.player.start_victory_walk()
        
        # Prevent monster from moving off screen
        for monster in self.monsters:
            if monster.rect.left < 0:
                monster.rect.left = 0
                monster.velocity_x *= -1
            elif monster.rect.right > self.background.get_width():
                monster.rect.right = self.background.get_width()
                monster.velocity_x *= -1
                
        # Prevent player moving off screen
        if self.player.rect.left < 0:
            self.player.rect.left = 0
            
        # Update camera to follow player
        self.camera.update(self.player)

    def pole_collision(self):
        if not self.player.is_sliding:
            self.player.start_pole_slide(self.pole.rect.centerx)
            self.flag.start_slide()
            
    def flag_collision(self):
        """Handle collision with the flag"""
        if not self.player.victory_dance:
            self.player.start_victory_walk()
            self.level_complete = True
            # Calculate time bonus
            time_bonus = self.time * 50
            self.score += time_bonus

    def draw(self, screen):
        screen.blit(self.background, self.camera.camera)
        
        # Clear UI
        self.UIManager.clear()

        # Left column
        self.UIManager.add_text('MARIO', (PADDING, PADDING))
        self.UIManager.add_text(f'{self.score:06d}', (PADDING, PADDING * 2.5))
        
        # Middle column  
        self.UIManager.add_text(f'COINS: {self.coins:02d}', (COLUMN_WIDTH + PADDING, PADDING))

        # Right column
        self.UIManager.add_text('TIME', (2 * COLUMN_WIDTH + PADDING, PADDING))
        self.UIManager.add_text(f'{self.time:03d}', (2 * COLUMN_WIDTH + PADDING, PADDING * 2.5))
        
        # Draw UI
        self.UIManager.draw()
        
        # Only need to draw platforms for debbuging
        """ for platform in self.platforms:
            if self.camera.camera.colliderect(platform.rect):
                pygame.draw.rect(screen, (139, 69, 19), self.camera.apply_rect(platform.rect)) """

        for tube in self.tubes:
            tube.draw(screen, self.camera)

        for block in self.blocks:
            block.draw(screen, self.camera)

        for monster in self.monsters:
            monster.draw(screen, self.camera)
            
        for block in self.blocks:
            if isinstance(block, BlockInt) and block.mushroom:
                block.mushroom.draw(screen, self.camera)
            elif isinstance(block, BlockInt) and block.coin:
                block.coin.draw(screen, self.camera)
            elif isinstance(block, BlockInt) and block.flower:
                block.flower.draw(screen, self.camera)
            
        self.pole.draw(screen, self.camera)
        self.flag.draw(screen, self.camera)
        
        self.player.draw(screen, self.camera)