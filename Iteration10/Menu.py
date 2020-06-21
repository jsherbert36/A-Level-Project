import math,pygame,random,sys,os
WHITE = (255,255,255)
BLACK = (0,0,0)
RED = (204,0,0)
PATH = sys.path[0]

class Button():
    def __init__(self,y_pos,size,text,action):
        self.size = size
        self.font = pygame.font.Font('freesansbold.ttf',self.size)
        self.colour = BLACK
        self.text = text
        self.object = self.font.render(self.text, True, self.colour)
        self.rect = self.object.get_rect()
        self.rect.centerx = SIZE[0]//2
        self.rect.centery = y_pos
        self.action = action

    def draw(self):
        screen.blit(self.object,self.rect)

    def update(self,mouse):
        if self.rect.collidepoint(mouse):
            self.colour = RED
        else:
            self.colour = BLACK
        self.object = self.font.render(self.text, True, self.colour)

def Menu1(window,surface):
    global SIZE,screen
    SIZE = window
    screen = surface
    choice = False
    button_size = 70
    button_list = []
    button_list.append(Button(SIZE[1]//2 - button_size*3,button_size,'Single Player','single'))
    button_list.append(Button(SIZE[1]//2 - button_size,button_size,'Two Player','double'))
    button_list.append(Button(SIZE[1]//2 + button_size,button_size,'AI Player','computer'))
    button_list.append(Button(SIZE[1]//2 + button_size*3,button_size,'Watch it Learn','learn'))
    background_image_1 = pygame.image.load(os.path.join(PATH,"images","Background.jpg")).convert()
    background_image_1 = pygame.transform.smoothscale(background_image_1, SIZE)
    clock = pygame.time.Clock()

    while not choice:
        screen.blit(background_image_1,(0,0)) 
        mouse = pygame.mouse.get_pos()      
        for button in button_list:
            button.update(mouse)
            button.draw()

        for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    choice = True
                    return 'gameover'
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        choice = True
                        return 'gameover'
                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    for button in button_list:
                        
                        if button.rect.collidepoint(mouse):
                            return button.action

        pygame.display.flip()       
        clock.tick(60)
