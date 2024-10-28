import pygame as pg

class Command:
    def execute():
        raise NotImplemented
    def undo():
        raise NotImplemented
    

class Up(Command):
    def execute():
        pass

    def undo():
        pass

class Down(Command):
    def execute():
        pass

    def undo():
        pass

class Left(Command):
    def execute():
        pass

    def undo():
        pass

class Right(Command):
    def execute():
        pass

    def undo():
        pass

class Shoot(Command):
    def execute():
        pass
    
    def undo():
        pass