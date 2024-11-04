from Observer import Observer

class PhysicsEngine(Observer):
    __instance = None
    
    @staticmethod
    def getInstance():
        if PhysicsEngine.__instance == None:
            PhysicsEngine()
        return PhysicsEngine.__instance
    
    def __init__(self):
        if PhysicsEngine.__instance != None:
            raise Exception("This class is a singleton!")
        else:
            PhysicsEngine.__instance = self
            super().__init__()

    def updatePlayerPosition(self, player):
        # Get player position
        # Check if player is falling through the floor
        # if player is falling through the floor, reposition player to the top of the floor
        pass
    
    def updateEnemyPosition(self, enemy):
        # Get enemy position
        # Check if enemy is falling through the floor
        # if enemy is falling through the floor, reposition enemy to the top of the floor
        pass
    
    def applyGravity(self, entity):
        # only apply gravity if entity is not on the floor and has reached its maximum height
        pass
    
    def checkPlayerCollision(self, player, enemy):
        # Check if player has collided with enemy
        # if player has collided with enemy, notify observers
        pass
    
    def update():
        # Update player position
        # Update enemy position
        # Apply gravity to player
        # Apply gravity to enemy
        # Check player collision with enemy
        pass