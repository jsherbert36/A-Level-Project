import math,pygame,random,sys,os
WHITE = (255,255,255)
BLACK = (0,0,0)
RED = (204,0,0)
PATH = sys.path[0]

class Button():
    def __init__(self,y_pos,size,text,action,active):
        self.size = size
        self.font = pygame.font.Font(os.path.join(PATH,"images","MenuFont.ttf"),self.size)
        self.colour = BLACK
        self.text = text
        self.object = self.font.render(self.text, True, self.colour)
        self.rect = self.object.get_rect()
        self.rect.centerx = SIZE[0]//2
        self.rect.centery = y_pos
        self.action = action
        self.active = active

    def draw(self):
        screen.blit(self.object,self.rect)

    def update(self,mouse):
        if self.rect.collidepoint(mouse):
            self.colour = RED
        else:
            self.colour = BLACK
        self.object = self.font.render(self.text, True, self.colour)

class Text_Box():
    def __init__(self,center,dimensions,text=''):
        self.rect = pygame.Rect(center[0] - dimensions[0]//2, centerr[1] - dimensions[1]//2, dimensions[0], dimensions[1])
        self.colour_inactive = BLACK
        self.colour_active = RED
        self.colour = self.colour_inactive
        self.text = text
        self.font = pygame.font.Font(os.path.join(PATH,"images","MenuFont.ttf"),self.rect // 1.1)
        self.font_surface = self.font.render(text, True, self.colour)
        self.active = False

    def mouse_event(self,event):
        if self.rect.collidepoint(event.pos):
            self.active = not self.active
        else:
            self.active = False
        if self.active:
            self.colour = self.colour_active
        else:
            self.colour = self.colour_inactive

    def key_event(self,event,keys):
        if self.active:
            if event.key == pygame.K_RETURN:
                return text
            elif keys[BACKSPACE]:
                self.text = self.text[:-1]
            elif len(self.text) < 20:
                self.text += event.unicode
            self.txt_surface = FONT.render(self.text, True, self.color)

    def update(self):
        self.rect.width = max(200, self.font_surface.get_width() + 10)

    def draw(self, screen):
        screen.blit(self.font_surface, (self.rect.x + 5, self.rect.y + 5))
        pygame.draw.rect(screen, self.color, self.rect, 4)


def Main_Menu(window,surface):
    global SIZE,screen
    SIZE = window
    screen = surface
    choice = False
    button_size = 90
    button_list = []
    button_list.append(Button(SIZE[1]//2 - button_size*3,button_size,'Single Player','single',True))
    button_list.append(Button(SIZE[1]//2 - button_size,button_size,'Two Player','double',True))
    button_list.append(Button(SIZE[1]//2 + button_size,button_size,'AI Player','computer',True))
    button_list.append(Button(SIZE[1]//2 + button_size*3,button_size,'Watch it Learn','learn',True))
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
                        if button.rect.collidepoint(mouse) and button.active:
                            return button.action

        pygame.display.flip()       
        clock.tick(60)

def Game_Over_Single(window,surface):
    global SIZE,screen
    SIZE = window
    screen = surface
    choice = False
    button_size = 90
    button_list = []
    username_box = Text_Box()
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
                        if button.rect.collidepoint(mouse) and button.active:
                            return button.action

        pygame.display.flip()       
        clock.tick(60)
