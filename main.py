from Game import Game
'''   
import pygame

def main(WIDTH, HEIGHT):
    pygame.init()

    GAME_EVENT = pygame.event.custom_type()
    display = pygame.display.set_mode((WIDTH, HEIGHT))
    clock = pygame.time.Clock()


    bg = pygame.image.load("img/level.png")

    mario = (4,0)

    cameraX = 0

    running = True

 
    while running:
        i = player_input()
        update()
        render()
        clock.tick(60)
 
        x, y = mario
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    x -= 1 

                elif event.key == pygame.K_RIGHT:
                    if(x >= WIDTH / 2):
                        cameraX -= 1.
                    else:
                        x += 1 
                    print(x, WIDTH / 2)
            elif event.type == GAME_EVENT:
                print(event.txt)

        display.blit(bg, (cameraX, 0))

        pygame.draw.rect(display, "red", (x, y))
        
        mario = (x,y)
        # Update the display
        pygame.display.update()
        # Control frame rate
        clock.tick(60)


    pygame.quit()
'''


if __name__ == "__main__":
    #main(800, 600)
    game = Game()
    game.start()