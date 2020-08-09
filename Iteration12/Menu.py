import math,pygame,random,sys,os
WHITE = (255,255,255)
BLACK = (0,0,0)
RED = (204,0,0)
GREY = (140, 140, 140)
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
        if self.rect.collidepoint(mouse) and self.active:
            self.colour = RED
        else:
            self.colour = BLACK
        self.object = self.font.render(self.text, True, self.colour)

class Text_Box():
    def __init__(self,center,dimensions,field=''):
        self.rect = pygame.Rect(center[0] - dimensions[0]//2, center[1] - dimensions[1]//2, dimensions[0], dimensions[1])
        self.colour_inactive = BLACK
        self.colour_active = RED
        self.colour = self.colour_inactive
        self.field = field
        self.text = self.field
        self.text_colour = GREY
        self.font = pygame.font.Font(os.path.join(PATH,"images","MenuFont.ttf"),int(self.rect.height//1.1))
        self.object = self.font.render(self.text, True, self.text_colour)
        self.active = False
        self.start = True
        self.original_width = self.rect.width

    def mouse_event(self,pos):
        if self.rect.collidepoint(pos):
            self.active = True
            if self.start == True:
                self.start = False
                self.text = ""
                self.text_colour = BLACK
        else:
            self.active = False
            if self.text == "":
                self.start = True
                self.text_colour = GREY
                self.text = self.field
        if self.active:
            self.colour = self.colour_active
        else:
            self.colour = self.colour_inactive

    def key_event(self,event,keys):
        if self.active:
            if event.key == pygame.K_RETURN:
                return self.text
            elif keys[pygame.K_BACKSPACE]:
                self.text = self.text[:-1]
            elif len(self.text) < 20:
                self.text += event.unicode

    def update(self,mouse):
        self.rect.width = max(self.original_width, self.object.get_width() + 10)
        self.rect.centerx = SIZE[0]//2
        if self.rect.collidepoint(mouse):
            self.colour = self.colour_active
        elif not self.active:
            self.colour = self.colour_inactive
        self.object = self.font.render(self.text, True, self.text_colour)

    def draw(self):
        screen.blit(self.object, (self.rect.x + 5, self.rect.y + 5))
        pygame.draw.rect(screen, self.colour, self.rect, 4)


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
    username_box = Text_Box([SIZE[0]//2,SIZE[1]//2],[200,button_size],"Username")
    button = Button(SIZE[1]//2 + button_size*3,button_size,'Watch it Learn','learn',False)
    background_image_1 = pygame.image.load(os.path.join(PATH,"images","Background.jpg")).convert()
    background_image_1 = pygame.transform.smoothscale(background_image_1, SIZE)
    clock = pygame.time.Clock()

    while not choice:
        mouse = pygame.mouse.get_pos() 
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                choice = True
                return 'gameover'
            elif event.type == pygame.KEYDOWN:
                username_box.key_event(event,pygame.key.get_pressed())
                if event.key == pygame.K_ESCAPE:
                    choice = True
                    return 'gameover'
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                username_box.mouse_event(mouse)                   
                if button.rect.collidepoint(mouse) and button.active:
                    return button.action
            screen.blit(background_image_1,(0,0))      
        button.update(mouse)
        button.draw()
        username_box.update(mouse)
        username_box.draw()
        pygame.display.flip()       
        clock.tick(60)


def leaderboard(window,surface):
    global SIZE,screen
    SIZE = window
    screen = surface
    choice = False
    button_size = 90
    button_list = []
    Title = Button(SIZE[1]//2 - button_size*3,button_size,'Leader Board       High Score','single',False)
    for user in users:
        button_list.append(Button(SIZE[1]//2 - button_size*3,button_size,user[0]+"        "+user[1],'single',False))

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

if __name__ == "__main__":
    os.environ['SDL_VIDEO_CENTERED'] = '1'
    pygame.init()
    infoObject = pygame.display.Info()
    SIZE = (infoObject.current_w, infoObject.current_h - 30)
    screen = pygame.display.set_mode(SIZE,pygame.RESIZABLE)
    pygame.display.set_caption("NEAT-JUMP")
    Game_Over_Single(SIZE,screen)