import pygame

PLATFORM_TYPES = {
    "normal": (139, 69, 19),    # Brown
    "grass": (34, 139, 34),     # Green
    "brick": (139, 0, 0),       # Red
    "ice": (135, 206, 235)      # Light blue
}

class Platform:
    def __init__(self, x, y, width, height):
        """Create a platform"""
        self.rect = pygame.Rect(x, y, width, height)
        self.color = (139, 69, 19)  # Brown color for more natural look
        self.type = "normal"  # Platform type for different behaviors
        
    def draw(self, screen, camera):
        """Draw the platform with camera offset"""
        pygame.draw.rect(screen, self.color, camera.apply_rect(self.rect))
        
    def update(self):
        if self.type == "moving":
            self.move()
        elif self.type == "breakable":
            self.check_break()
    
    @property
    def bottom(self):
        return self.rect.bottom
    
    @property
    def top(self):
        return self.rect.top
    
    @property
    def left(self):
        return self.rect.left
    
    @property
    def right(self):
        return self.rect.right