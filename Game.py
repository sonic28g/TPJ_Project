import pygame
from GameVariables import FPS,WINDOW_W,WINDOW_H
from PhysicsEngine import PhysicsEngine
from GraphicsEngine import GraphicsEngine
from World import World
from Command import InputHandler

class Game:
    def __init__(self):
        pygame.init()
        
        self.GAME_EVENT = pygame.event.custom_type()
        self.display = pygame.display.set_mode((WINDOW_W, WINDOW_H))
        self.clock = pygame.time.Clock()
        self.running = True
        self.graphicsEngine = GraphicsEngine(self.display)
        self.physicsEngine = PhysicsEngine()
        self.world = self.initWorld("assets/img/level.png")
        self.inputHandler = InputHandler(self.world.player)

    
    def initWorld(self, world):
        world = World(world)
        return world
        
    def start(self):

        while self.running:
            self.input()
            self.update()
            self.render()
            self.clock.tick(FPS)

    def input(self):
        keys = pygame.key.get_pressed()
    
        if not any(keys):  # If no keys are pressed
            self.inputHandler.handleInput("nothing")

        if keys[pygame.K_LEFT]:
            self.inputHandler.handleInput("a")

        if keys[pygame.K_RIGHT]:
            self.inputHandler.handleInput("d")

        if keys[pygame.K_UP]:
            pass

        if keys[pygame.K_DOWN]:
            pass

        if keys[pygame.K_SPACE]:
            pass

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

            elif event.type == self.GAME_EVENT:
                print(event.txt)

    def update(self):
        self.world.update()
        

    def render(self):
        """ self.display.blit(self.world.level, (0, 0))
        pygame.display.update() """
        
        self.display.fill((0, 0, 0))  # Clear screen

        # Get camera offset
        camera_x, camera_y = self.world.getCameraOffset()

        # Render level
        level_pos = (-camera_x, -camera_y)
        self.display.blit(self.world.level, level_pos)

        # Render player
        player_screen_pos = self.world.camera.apply(self.world.player)
        self.graphicsEngine.drawPlayer(self.world.player)

        # Render mobs
        for mob in self.world.mobs:
            mob_screen_pos = self.world.camera.apply(mob)
            self.graphicsEngine.draw_mob(mob_screen_pos)

        # Render blocks
        for block in self.world.blocks:
            block_screen_pos = self.world.camera.apply(block)
            self.graphicsEngine.draw_block(block_screen_pos)

        # ... render other game elements ...

        pygame.display.flip()

    