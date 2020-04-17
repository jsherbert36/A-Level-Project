import math,pygame,random,sys,os
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
PATH = sys.path[0]
import numpy as np

def gameover():
    font = pygame.font.Font('freesansbold.ttf', 70) 
    exit = False
    clock = pygame.time.Clock()
    while not exit:
        screen.fill(BLACK) 
        Play = font.render('GAME OVER', True, WHITE)
        PlayRect = Play.get_rect()
        PlayRect.center = (size[0]//2, size[1]//2)
        screen.blit(Play, PlayRect) 
        pygame.display.flip()
        for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit = True
                    pygame.quit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        exit = True
                        pygame.quit()
            
        clock.tick(60)

if __name__ == "__main__":
    pygame.init()
    size = (1280,720)
    screen = pygame.display.set_mode(size)
    background_image_1 = pygame.image.load(os.path.join(PATH,"images","Background.jpg")).convert()
    background_image_1 = pygame.transform.smoothscale(background_image_1, size)
    gameover()
    pygame.quit()