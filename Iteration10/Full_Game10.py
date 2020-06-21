import math,pygame,random,sys,os,Menu,GameOver,SinglePlayer,DoublePlayer,NEAT
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
PATH = sys.path[0]

if __name__ == "__main__":
    os.environ['SDL_VIDEO_CENTERED'] = '1'
    pygame.init()
    SIZE = (1280,720)
    screen = pygame.display.set_mode(SIZE)
    pygame.display.set_caption("NEAT-JUMP")
    choice = None
    while choice != 'gameover':
        choice = Menu.Menu1(SIZE,screen)
        if choice == 'single':
            result = SinglePlayer.gameplay(SIZE,screen)
        elif choice == 'double':
            result = DoublePlayer.gameplay(SIZE,screen)
        elif choice == 'computer':
            pass
        elif choice == 'learn':
            result = NEAT.run(os.path.join(PATH,"config2.txt"),SIZE,screen)
    pygame.quit()