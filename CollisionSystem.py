import pygame
from Powerup import Mushroom, Flower
from Block import BlockInt, BlockBreak
from Settings import *
from Monster import Koopa, Goomba

class CollisionTypes:
    """Constants for collision types"""
    PLAYER_POWERUP = "player_powerup"
    POWERUP_PLATFORM = "powerup_platform"
    POWERUP_TUBE = "powerup_tube"
    POWERUP_BLOCK = "powerup_block"
    PLAYER_MONSTER = "player_monster"
    MONSTER_PLATFORM = "monster_platform"
    MONSTER_TUBE = "monster_tube"
    PLAYER_PLATFORM = "player_platform"
    PLAYER_TUBE = "player_tube"
    PLAYER_BLOCK = "player_block"
    PLAYER_POLE = "player_pole"
    PLAYER_FLAG = "player_flag"

class CollisionObserver:
    """Base class for collision observers"""
    def on_notify(self, entity1, entity2, collision_type):
        pass

class PowerUpCollisionHandler(CollisionObserver):
    def __init__(self, world):
        self.world = world
        
    def on_notify(self, powerup, other, collision_type):
        if collision_type == CollisionTypes.PLAYER_POWERUP:
            self._handle_player_collision(powerup, other)
        elif collision_type == CollisionTypes.POWERUP_PLATFORM:
            self._handle_platform_collision(powerup, other)
        elif collision_type == CollisionTypes.POWERUP_TUBE:
            self._handle_tube_collision(powerup, other)
        elif collision_type == CollisionTypes.POWERUP_BLOCK:
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
            
        if powerup.velocity_y > 0:
            powerup.rect.bottom = platform.rect.top
            powerup.velocity_y = 0
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

class MonsterCollisionHandler(CollisionObserver):
    def __init__(self, world):
        self.world = world
        
    def on_notify(self, monster, other, collision_type):
        if collision_type == CollisionTypes.PLAYER_MONSTER:
            self._handle_player_collision(monster, other)
        elif collision_type == CollisionTypes.MONSTER_PLATFORM:
            self._handle_platform_collision(monster, other)
        elif collision_type == CollisionTypes.MONSTER_TUBE:
            self._handle_tube_collision(monster, other)
            
    def _handle_player_collision(self, monster, player):
        if player.velocity_y > 0 and player.rect.bottom < monster.rect.centery + 10:
            if isinstance(monster, Koopa):
                if not monster.is_shell:
                    monster.convert_to_shell()
                    player.velocity_y = -15
                    self.world.score += 100
                else:
                    if monster.velocity_x != 0:
                        monster.velocity_x = 0
                    else:
                        direction = 1 if player.rect.centerx < monster.rect.centerx else -1
                        monster.kick_shell(direction)
                    player.velocity_y = -10
                    self.world.score += 100
            else:
                monster.die()
                player.velocity_y = -15
                self.world.score += 100
        elif monster.is_alive or (isinstance(monster, Koopa) and monster.is_shell and monster.velocity_x != 0):
            if player.is_big:
                player.take_damage()
            else:
                self.world.player_die()
                
    def _handle_platform_collision(self, monster, platform):
        if monster.velocity_y > 0:
            monster.rect.bottom = platform.rect.top
            monster.velocity_y = 0
        elif monster.velocity_y < 0:
            monster.rect.top = platform.rect.bottom
            monster.velocity_y = 0
        elif monster.rect.right > platform.rect.left and monster.rect.left < platform.rect.left:
            monster.rect.right = platform.rect.left
            monster.velocity_x *= -1
        elif monster.rect.left < platform.rect.right and monster.rect.right > platform.rect.right:
            monster.rect.left = platform.rect.right
            monster.velocity_x *= -1
            
    def _handle_tube_collision(self, monster, tube):
        if monster.velocity_y > 0 and monster.rect.bottom < tube.rect.centery:
            monster.rect.bottom = tube.rect.top
            monster.velocity_y = 0
        elif monster.rect.right > tube.rect.left and monster.rect.left < tube.rect.left:
            monster.rect.right = tube.rect.left
            monster.velocity_x *= -1
        elif monster.rect.left < tube.rect.right and monster.rect.right > tube.rect.right:
            monster.rect.left = tube.rect.right
            monster.velocity_x *= -1
         
class CollisionSystem:
    """Main collision system that detects and notifies about collisions"""
    def __init__(self):
        self.observers = []
        
    def add_observer(self, observer):
        self.observers.append(observer)
        
    def remove_observer(self, observer):
        self.observers.remove(observer)
        
    def notify(self, entity1, entity2, collision_type):
        for observer in self.observers:
            observer.on_notify(entity1, entity2, collision_type)
            
    def check_collisions(self, world):
        # Check powerup collisions
        self._check_powerup_collisions(world)
        
        # Check player collisions
        self._check_player_collisions(world)
        
        # Check monster collisions
        self._check_monster_collisions(world)
        
    def _check_powerup_collisions(self, world):
        for block in world.blocks:
            if not isinstance(block, BlockInt): continue
            for powerup in [block.mushroom, block.flower]:
                if not (powerup and powerup.is_active): continue
                
                if powerup.rect.colliderect(world.player.rect):
                    self.notify(powerup, world.player, CollisionTypes.PLAYER_POWERUP)
                    
                if not isinstance(powerup, Mushroom): continue
                
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
            
    def _check_monster_collisions(self, world):
        for monster in world.monsters:
            if monster.rect.colliderect(world.player.rect):
                self.notify(monster, world.player, CollisionTypes.PLAYER_MONSTER)
                
            for platform in world.platforms:
                if monster.rect.colliderect(platform.rect):
                    self.notify(monster, platform, CollisionTypes.MONSTER_PLATFORM)
                    
            for tube in world.tubes:
                if monster.rect.colliderect(tube.rect):
                    self.notify(monster, tube, CollisionTypes.MONSTER_TUBE)