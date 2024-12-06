import pygame

class Camera:
    def __init__(self, width, height):
        """Initialize camera"""
        self.camera = pygame.Rect(0, 0, width, height)
        self.width = width
        self.height = height

    def apply(self, entity):
        """Apply camera offset to an entity"""
        return entity.rect.move(self.camera.topleft)

    def apply_rect(self, rect):
        """Apply camera offset to a rectangle"""
        return rect.move(self.camera.topleft)

    def update(self, target):
        """Update camera position to follow target"""
        # Center the camera on the target
        x = -target.rect.centerx + self.width // 2
        y = -target.rect.centery + self.height // 2

        # Limit scrolling to map boundaries
        x = min(0, x)  # Left boundary
        y = min(0, y)  # Top boundary
        
        # Assuming a large map width and height - adjust these as needed
        x = max(-(12660 - self.width), x)  # Right boundary
        y = max(-(900 - self.height), y)  # Bottom boundary

        self.camera = pygame.Rect(x, y, self.width, self.height)
        
    def other_function():
        pass
