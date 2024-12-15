import pygame
from Settings import GRAVITY

class PowerUp(pygame.sprite.Sprite):
    """Base power-up class that provides a sandbox of operations for subclasses"""
    def __init__(self, block_x, block_y):
        super().__init__()
        # Core attributes
        self.image = None
        self.rect = pygame.Rect(0, 0, 48, 48)
        self._setup_position(block_x, block_y)
        
        # Movement and state
        self.velocity_x = 0
        self.velocity_y = 0
        self.is_active = False
        self.is_emerging = True
        self.emergence_height = 0
        
    def _setup_position(self, block_x, block_y):
        """Protected operation for initial positioning relative to block"""
        self.rect.centerx = block_x + 30
        self.rect.centery = block_y + 30
        
    def update(self):
        """Main sandbox method controlling the power-up behavior"""
        if self.is_active:
            if self.is_emerging:
                self._handle_emergence()
            else:
                self._handle_movement()
                self._handle_animation()
    
    def _handle_emergence(self):
        """Protected operation for emergence animation"""
        if self.emergence_height < self._get_emergence_limit():
            self.rect.y -= 2
            self.emergence_height += 2
        else:
            self.is_emerging = False
            self._on_emergence_complete()
    
    def _handle_movement(self):
        """Protected operation for physics - can be overridden"""
        self.velocity_y += GRAVITY
        self.rect.x += self.velocity_x
        self.rect.y += self.velocity_y
    
    def _handle_animation(self):
        """Protected operation for animation - to be overridden by animated power-ups"""
        pass
    
    def _get_emergence_limit(self):
        """Protected operation for emergence height - can be overridden"""
        return 48
    
    def _on_emergence_complete(self):
        """Protected hook for emergence completion behavior"""
        pass
    
    def draw(self, screen, camera):
        """Provided operation for rendering"""
        if self.is_active:
            screen.blit(self.image, camera.apply(self))

    def activate(self):
        """Public method to activate the power-up"""
        self.is_active = True

class Mushroom(PowerUp):
    def __init__(self, block_x, block_y):
        super().__init__(block_x, block_y)
        self.image = pygame.image.load('assets/items/mushroom.png').convert_alpha()
        self.image = pygame.transform.scale(self.image, (48, 48))
        
    def _on_emergence_complete(self):
        """Mushroom moves horizontally after emerging"""
        self.velocity_x = 3
        self.velocity_y = -10

class Flower(PowerUp):
    def __init__(self, block_x, block_y):
        super().__init__(block_x, block_y)
        # Initialize animation sprites
        self.sprites = []
        for i in range(4):
            sprite = pygame.image.load(f'assets/items/flower{i}.png').convert_alpha()
            self.sprites.append(pygame.transform.scale(sprite, (48, 48)))
        
        self.current_sprite = 0
        self.animation_speed = 0.15
        self.image = self.sprites[self.current_sprite]
    
    def _handle_movement(self):
        """Flower doesn't move after emerging"""
        pass
    
    def _handle_animation(self):
        """Handle flower animation"""
        self.current_sprite += self.animation_speed
        if self.current_sprite >= len(self.sprites):
            self.current_sprite = 0
        self.image = self.sprites[int(self.current_sprite)]
    
    def _get_emergence_limit(self):
        return 53