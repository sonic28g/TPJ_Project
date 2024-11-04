import pygame as pg

class Command:
    def execute(self):
        raise NotImplementedError("Subclasses must implement this method")
    
class Up(Command):
    def execute(self):
        print("Up")
        
class Down(Command):
    def execute(self):
        print("Down")
        
class Left(Command):
    def execute(self):
        print("Left")
        
class Right(Command):
    def execute(self):
        print("Right")
        
class InputHandler:
    command = {
        "w": Up(),
        "s": Down(),
        "a": Left(),
        "d": Right()
    }
    
    def handleInput(self, key):
        self.command[key].execute()