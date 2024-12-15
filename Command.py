import pygame

class Command:
    """Base command class"""
    def execute(self, player):
        pass

    def undo(self):
        pass

class JumpCommand(Command):
    def execute(self, player):
        if not player.is_jumping:
            player.jump()

    def undo(self, player):
        player.release_jump()

class ReleaseJumpCommand(Command):
    def execute(self, player):
        player.release_jump()

class MoveCommand(Command):
    def __init__(self, left, right):
        self.left = left
        self.right = right

    def execute(self, player):
        player.move(self.left, self.right)

class InputHandler:
    def __init__(self):
        self.commands = {}
        self.setup_commands()

    def setup_commands(self):
        # Map keys to commands
        self.commands[pygame.K_SPACE] = JumpCommand()
        # Movement will be handled separately as it needs continuous input state

    def handle_keydown(self, event, player):
        if event.key in self.commands:
            self.commands[event.key].execute(player)

    def handle_keyup(self, event, player):
        if event.key == pygame.K_SPACE:
            ReleaseJumpCommand().execute(player)

    def handle_continuous_input(self, player):
        keys = pygame.key.get_pressed()
        left = keys[pygame.K_LEFT] or keys[pygame.K_a]
        right = keys[pygame.K_RIGHT] or keys[pygame.K_d]
        MoveCommand(left, right).execute(player)