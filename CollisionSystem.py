# collision_system.py
from typing import List, Any
import pygame
from Goomba import Goomba
from Koopa import Koopa
from Powerup import Mushroom, Flower
from Block import BlockInt, BlockBreak

class CollisionTypes:
    """Constants for collision types"""
    PLAYER_POWERUP = "player_powerup"
    POWERUP_PLATFORM = "powerup_platform"
    POWERUP_TUBE = "powerup_tube"
    POWERUP_BLOCK = "powerup_block"
    PLAYER_ENEMY = "player_enemy"
    ENEMY_PLATFORM = "enemy_platform"
    ENEMY_TUBE = "enemy_tube"
    PLAYER_PLATFORM = "player_platform"
    PLAYER_TUBE = "player_tube"
    PLAYER_BLOCK = "player_block"
    PLAYER_POLE = "player_pole"
    PLAYER_FLAG = "player_flag"

class CollisionObserver:
    """Base class for collision observers"""
    def on_notify(self, entity1: Any, entity2: Any, collision_type: str) -> None:
        pass

class PowerUpCollisionHandler(CollisionObserver):
    def __init__(self, world):
        self.world = world
        
    def on_notify(self, powerup, other, collision_type):
        if collision_type == "player":
            self._handle_player_collision(powerup, other)
        elif collision_type == "platform":
            self._handle_platform_collision(powerup, other)
        elif collision_type == "tube":
            self._handle_tube_collision(powerup, other)
        elif collision_type == "block":
            self._handle_block_collision(powerup, other)
            
    def _handle_player_collision(self, powerup, player):
        # Find the block that contains this powerup
        for block in self.world.blocks:
            if isinstance(block, BlockInt):
                if powerup == block.mushroom:
                    block.mushroom = None
                elif powerup == block.flower:
                    block.flower = None
                if block.mushroom is None and block.flower is None:
                    player.grow()
                    self.world.score += 1000
                    break
                    
    def _handle_platform_collision(self, powerup, platform):
        if not isinstance(powerup, Mushroom):
            return
            
        # Handle vertical collision
        if powerup.velocity_y > 0:
            print("powerup.rect.bottom: ", powerup.rect.bottom)
            powerup.rect.bottom = platform.rect.top
            powerup.velocity_y = 0
        
        # Handle horizontal collisions
        elif powerup.velocity_x > 0:
            powerup.rect.right = platform.rect.left
            powerup.velocity_x *= -1
        elif powerup.velocity_x < 0:
            powerup.rect.left = platform.rect.right
            powerup.velocity_x *= -1
            
    def _handle_tube_collision(self, powerup, tube):
        if not isinstance(powerup, Mushroom):
            return
            
        if powerup.velocity_y > 0:
            powerup.rect.bottom = tube.rect.top
            powerup.velocity_y = 0
        elif powerup.rect.right > tube.rect.left and powerup.rect.left < tube.rect.left:
            powerup.rect.right = tube.rect.left
            powerup.velocity_x *= -1
        elif powerup.rect.left < tube.rect.right and powerup.rect.right > tube.rect.right:
            powerup.rect.left = tube.rect.right
            powerup.velocity_x *= -1
            
    def _handle_block_collision(self, powerup, block):
        if not isinstance(powerup, Mushroom) or powerup.is_emerging:
            return
            
        if powerup.velocity_y > 0:
            powerup.rect.bottom = block.rect.top
            powerup.velocity_y = 0
        elif powerup.rect.right > block.rect.left and powerup.rect.left < block.rect.left:
            powerup.rect.right = block.rect.left
            powerup.velocity_x *= -1
        elif powerup.rect.left < block.rect.right and powerup.rect.right > block.rect.right:
            powerup.rect.left = block.rect.right
            powerup.velocity_x *= -1

class PlayerCollisionHandler(CollisionObserver):
    def __init__(self, world):
        self.world = world
    
    def on_notify(self, player, other, collision_type):
        if collision_type == CollisionTypes.PLAYER_PLATFORM:
            self._handle_platform_collision(player, other)
        elif collision_type == CollisionTypes.PLAYER_TUBE:
            self._handle_tube_collision(player, other)
        elif collision_type == CollisionTypes.PLAYER_BLOCK:
            self._handle_block_collision(player, other)
        elif collision_type == CollisionTypes.PLAYER_POLE:
            self._handle_pole_collision(player, other)
        elif collision_type == CollisionTypes.PLAYER_FLAG:
            self._handle_flag_collision(player, other)
            
    def _handle_platform_collision(self, player, platform):
        if (player.velocity_y > 0 and 
            player.rect.right > platform.rect.left + 10 and 
            player.rect.left < platform.rect.right - 10):
            player.rect.bottom = platform.rect.top
            player.velocity_y = 0
            player.is_jumping = False
        elif player.velocity_y < 0:
            player.rect.top = platform.rect.bottom
            player.velocity_y = 0
        elif player.rect.right > platform.rect.left and player.rect.left < platform.rect.left:
            player.rect.right = platform.rect.left
        elif player.rect.left < platform.rect.right and player.rect.right > platform.rect.right:
            player.rect.left = platform.rect.right
            
    def _handle_tube_collision(self, player, tube):
        if (player.rect.top < tube.rect.top and 
            player.velocity_y > 0 and 
            player.rect.right > tube.rect.left + 5 and 
            player.rect.left < tube.rect.right - 5):
            player.rect.bottom = tube.rect.top
            player.velocity_y = 0
            player.is_jumping = False
        elif player.rect.right > tube.rect.left and player.rect.left < tube.rect.left:
            player.rect.right = tube.rect.left
        elif player.rect.left < tube.rect.right and player.rect.right > tube.rect.right:
            player.rect.left = tube.rect.right
            
    def _handle_block_collision(self, player, block):
        if (player.rect.top < block.rect.top and 
            player.velocity_y > 0 and 
            player.rect.right > block.rect.left + 5 and 
            player.rect.left < block.rect.right - 5):
            player.rect.bottom = block.rect.top
            player.velocity_y = 0
            player.is_jumping = False
        elif (player.rect.bottom > block.rect.bottom and 
              player.velocity_y < 0 and 
              player.rect.right > block.rect.left + 5 and 
              player.rect.left < block.rect.right - 5):
            player.rect.top = block.rect.bottom
            player.velocity_y = 0
            player.holding_jump = False
            player.jump_force = 0
            block.hit(player.is_big)
        elif player.rect.right > block.rect.left and player.rect.left < block.rect.left:
            player.rect.right = block.rect.left
        elif player.rect.left < block.rect.right and player.rect.right > block.rect.right:
            player.rect.left = block.rect.right
            
    def _handle_pole_collision(self, player, pole):
        if not player.is_sliding:
            player.start_pole_slide(pole.rect.centerx)
            
    def _handle_flag_collision(self, player, flag):
        if not player.victory_dance:
            player.start_victory_walk()
            self.world.level_complete = True
            self.world.score += self.world.time * 50

class EnemyCollisionHandler(CollisionObserver):
    def __init__(self, world):
        self.world = world
        
    def on_notify(self, enemy, other, collision_type):
        if collision_type == CollisionTypes.PLAYER_ENEMY:
            self._handle_player_collision(enemy, other)
        elif collision_type == CollisionTypes.ENEMY_PLATFORM:
            self._handle_platform_collision(enemy, other)
        elif collision_type == CollisionTypes.ENEMY_TUBE:
            self._handle_tube_collision(enemy, other)
            
    def _handle_player_collision(self, enemy, player):
        if player.velocity_y > 0 and player.rect.bottom < enemy.rect.centery + 10:
            if isinstance(enemy, Koopa):
                if not enemy.is_shell:
                    enemy.convert_to_shell()
                    player.velocity_y = -15
                    self.world.score += 100
                else:
                    if enemy.velocity_x != 0:
                        enemy.velocity_x = 0
                    else:
                        direction = 1 if player.rect.centerx < enemy.rect.centerx else -1
                        enemy.kick_shell(direction)
                    player.velocity_y = -10
                    self.world.score += 100
            else:
                enemy.die()
                player.velocity_y = -15
                self.world.score += 100
        elif enemy.is_alive or (isinstance(enemy, Koopa) and enemy.is_shell and enemy.velocity_x != 0):
            if player.is_big:
                player.take_damage()
            else:
                self.world.player_die()
                
    def _handle_platform_collision(self, enemy, platform):
        if enemy.velocity_y > 0:
            enemy.rect.bottom = platform.rect.top
            enemy.velocity_y = 0
        elif enemy.velocity_y < 0:
            enemy.rect.top = platform.rect.bottom
            enemy.velocity_y = 0
        elif enemy.rect.right > platform.rect.left and enemy.rect.left < platform.rect.left:
            enemy.rect.right = platform.rect.left
            enemy.velocity_x *= -1
        elif enemy.rect.left < platform.rect.right and enemy.rect.right > platform.rect.right:
            enemy.rect.left = platform.rect.right
            enemy.velocity_x *= -1
            
    def _handle_tube_collision(self, enemy, tube):
        if enemy.velocity_y > 0 and enemy.rect.bottom < tube.rect.centery:
            enemy.rect.bottom = tube.rect.top
            enemy.velocity_y = 0
        elif enemy.rect.right > tube.rect.left and enemy.rect.left < tube.rect.left:
            enemy.rect.right = tube.rect.left
            enemy.velocity_x *= -1
        elif enemy.rect.left < tube.rect.right and enemy.rect.right > tube.rect.right:
            enemy.rect.left = tube.rect.right
            enemy.velocity_x *= -1

class CollisionSystem:
    def __init__(self):
        self.observers: List[CollisionObserver] = []
        
    def add_observer(self, observer: CollisionObserver) -> None:
        self.observers.append(observer)
        
    def notify(self, entity1: Any, entity2: Any, collision_type: str) -> None:
        for observer in self.observers:
            observer.on_notify(entity1, entity2, collision_type)
            
    def check_collisions(self, world) -> None:
        # Check powerup collisions
        self._check_powerup_collisions(world)
        
        # Check player collisions
        self._check_player_collisions(world)
        
        # Check enemy collisions
        self._check_enemy_collisions(world)
    
    def _check_powerup_collisions(self, world):
        for block in world.blocks:
            if not isinstance(block, BlockInt):
                continue
            
            for powerup in [block.mushroom, block.flower]:
                if not (powerup and powerup.is_active):
                    continue
                
                if powerup.rect.colliderect(world.player.rect):
                    self.notify(powerup, world.player, CollisionTypes.PLAYER_POWERUP)
                    
                if not isinstance(powerup, Mushroom):
                    continue
                
                for platform in world.platforms:
                    if powerup.rect.colliderect(platform.rect):
                        self.notify(powerup, platform, CollisionTypes.POWERUP_PLATFORM)
                        
                for tube in world.tubes:
                    if powerup.rect.colliderect(tube.rect):
                        self.notify(powerup, tube, CollisionTypes.POWERUP_TUBE)
                        
                for other_block in world.blocks:
                    if powerup.rect.colliderect(other_block.rect):
                        self.notify(powerup, other_block, CollisionTypes.POWERUP_BLOCK)
    
    def _check_player_collisions(self, world):
        player = world.player
        
        for platform in world.platforms:
            if player.rect.colliderect(platform.rect):
                self.notify(player, platform, CollisionTypes.PLAYER_PLATFORM)
                
        for tube in world.tubes:
            if player.rect.colliderect(tube.rect):
                self.notify(player, tube, CollisionTypes.PLAYER_TUBE)
                
        for block in world.blocks:
            if isinstance(block, BlockBreak) and not block.active:
                continue
            if player.rect.colliderect(block.rect):
                self.notify(player, block, CollisionTypes.PLAYER_BLOCK)
                
        if player.rect.colliderect(world.pole.rect):
            self.notify(player, world.pole, CollisionTypes.PLAYER_POLE)
            
        if player.rect.colliderect(world.flag.rect):
            self.notify(player, world.flag, CollisionTypes.PLAYER_FLAG)
    
    def _check_enemy_collisions(self, world):
        for enemy in world.monsters:
            if enemy.rect.colliderect(world.player.rect):
                self.notify(enemy, world.player, CollisionTypes.PLAYER_ENEMY)
                
            for platform in world.platforms:
                if enemy.rect.colliderect(platform.rect):
                    self.notify(enemy, platform, CollisionTypes.ENEMY_PLATFORM)
                    
            for tube in world.tubes:
                if enemy.rect.colliderect(tube.rect):
                    self.notify(enemy, tube, CollisionTypes.ENEMY_TUBE)