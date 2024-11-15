class GraphicsEngine:
    def __init__(self, window):
        self.window = window
        
    def drawWorld(self, world):
        self.window.blit(world.level.backgroundImage, (0, 0))
            
    def drawPlayer(self, player):
        self.window.blit(player.currentSprite, player.rect)
        
    def drawMobs(self, monsters):
        for monster in monsters:
            self.window.blit(monster.image, monster.rect)
            
    def draw(self, world):
        self.drawWorld(world)
        self.drawPlayer(world.player)
        self.drawMobs(world.mobs)
        
    def update(self):
        pass