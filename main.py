import pygame


def main(WIDTH, HEIGHT, SCALE=32):
    pygame.init()

  
    display = pygame.display.set_mode((SCALE * WIDTH, SCALE * HEIGHT))
    clock = pygame.time.Clock()

   
    pygame.quit()


if __name__ == "__main__":
    main(40, 20)