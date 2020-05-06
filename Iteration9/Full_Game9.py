import math,pygame,random,sys,os,Menu,GameOver,GamePlay,NEAT
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
PATH = sys.path[0]
import numpy as np

if __name__ == "__main__":
    pygame.init()
    SIZE = (1280,720)
    screen = pygame.display.set_mode(SIZE)
    pygame.display.set_caption("NEAT-JUMP")
    choice = None
    while choice != 'gameover':
        choice = Menu.Menu1(SIZE,screen)
        if choice == 'single':
            result = GamePlay.gameplay(SIZE,screen,'single')
        elif choice == 'double':
            result = GamePlay.gameplay(SIZE,screen,'double')
        elif choice == 'computer':
            pass
        elif choice == 'learn':
            result = NEAT.run(os.path.join(PATH,"config2.txt"),SIZE,screen)
    pygame.quit()