import math,pygame,random,sys,os,Menu,SinglePlayer,DoublePlayer,NEAT
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
PATH = sys.path[0]
os.environ['SDL_VIDEO_CENTERED'] = '1'
pygame.init()
infoObject = pygame.display.Info()
SIZE = (infoObject.current_w - 100, infoObject.current_h - 100)
screen = pygame.display.set_mode(SIZE,pygame.NOFRAME,0)
pygame.display.set_caption("NEAT JUMP")
pygame.display.set_icon(pygame.image.load(os.path.join(PATH,"images",("frame-1.png"))).convert_alpha())
choice = None
result = None
while choice != 'gameover'and result != "gameover":
    choice = Menu.main_menu(SIZE,screen)
    if choice == 'single':
        result = SinglePlayer.gameplay(SIZE,screen)
    elif choice == 'double':
        result = DoublePlayer.gameplay(SIZE,screen)
    elif choice == 'computer':
        pass
    elif choice == 'learn':
        result = NEAT.run(SIZE,screen)
    elif choice == 'leaderboard':
        result = Menu.leaderboard(SIZE,screen)
pygame.quit()