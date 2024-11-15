class Camera:
    def __init__(self, window_width, window_height, level_width, level_height):
        self.width = window_width
        self.height = window_height
        self.level_width = level_width
        self.level_height = level_height
        self.x = 0
        self.y = 0
        
        # Define the deadzone (center 1/3 of the screen)
        self.deadzone_left = window_width / 3
        self.deadzone_right = window_width * 2 / 3

    def update(self, player_x, player_y):
        # Horizontal camera movement
        if player_x < self.x + self.deadzone_left:
            self.x = player_x - self.deadzone_left
        elif player_x > self.x + self.deadzone_right:
            self.x = player_x - self.deadzone_right
        
        # Vertical camera movement (simple centering)
        self.y = player_y - self.height / 2
        
        # Ensure camera doesn't show area outside the level
        self.x = max(0, min(self.x, self.level_width - self.width))
        self.y = max(0, min(self.y, self.level_height - self.height))

    def apply(self, entity):
        return entity.posX - self.x, entity.posY - self.y