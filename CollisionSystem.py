import pygame
from Powerup import Mushroom, Flower
from Block import BlockInt

class CollisionObserver:
    """Base class for collision observers"""
    def on_notify(self, entity1, entity2, collision_type):
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
        # Check power-up collisions
        for block in world.blocks:
            if isinstance(block, BlockInt):
                for powerup in [block.mushroom, block.flower]:
                    if powerup and powerup.is_active:
                        # Check player collision
                        if powerup.rect.colliderect(world.player.rect):
                            self.notify(powerup, world.player, "player")
                            
                        # Only check physical collisions for mushrooms
                        if isinstance(powerup, Mushroom):
                            # Platform collisions
                            for platform in world.platforms:
                                if powerup.rect.colliderect(platform.rect):
                                    self.notify(powerup, platform, "platform")
                                    
                            # Tube collisions
                            for tube in world.tubes:
                                if powerup.rect.colliderect(tube.rect):
                                    self.notify(powerup, tube, "tube")
                                    
                            # Block collisions
                            for other_block in world.blocks:
                                if powerup.rect.colliderect(other_block.rect):
                                    self.notify(powerup, other_block, "block")