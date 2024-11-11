class Command:
    def __init__(self):
        self.execute = None
    

class Up(Command):
    def __init__(self, actor):
        self.execute = actor.up
        
class Down(Command):
    def __init__(self, actor):
        self.execute = actor.Down
        
class Left(Command):
    def __init__(self, actor):
        self.execute = actor.left
        
class Right(Command):
    def __init__(self, actor):
        self.execute = actor.right

class Shoot(Command):
    def __init__(self, actor):
        self.execute = actor.shoot
        
        
class InputHandler:

    def __init__(self, actor):
    
        self.command = {
            "w": Up(actor),
            "s": Down(actor),
            "a": Left(actor),
            "d": Right(actor),
            "space": Shoot(actor)
        }
    
    def handleInput(self, key):
        self.command[key].execute()