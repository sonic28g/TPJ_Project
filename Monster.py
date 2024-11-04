class Monster:
    def __init__(self) -> None:
        self.positionX = 0
        self.positionY = 0
        self.rect = None
        self.velocityX = 0
        self.velociyY = 0
        self.isAlive = True
        self.sprites = []
        
    def clone(self) -> Monster:
        return NotImplemented
    
class Koopa(Monster):
    def __init__(self) -> None:
        super().__init__()
    
    def clone(self) -> Monster:
        return Koopa()
    
class Goomba(Monster):
    def __init__(self) -> None:
        super().__init__()
        
    def clone(self) -> Monster:
        return Goomba()
    
class Spawner:
    def spawnMonster(self, prototype) -> Monster:
        return prototype.clone()