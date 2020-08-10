import math,pygame,random,sys,os,json
WHITE = (255,255,255)
BLACK = (0,0,0)
RED = (204,0,0)
GREY = (140, 140, 140)
PATH = sys.path[0]

class Button():
    def __init__(self,y_pos,size,text,action,active,color = BLACK):
        self.size = size
        self.font = pygame.font.Font(os.path.join(PATH,"fonts","Folks-Bold.ttf"),self.size)
        self.default_color = color
        self.color = self.default_color
        self.text = text
        self.object = self.font.render(self.text, True, self.color)
        self.rect = self.object.get_rect()
        self.rect.centerx = SIZE[0]//2
        self.rect.centery = y_pos
        self.action = action
        self.active = active

    def draw(self):
        screen.blit(self.object,self.rect)

    def update(self,mouse):
        if self.rect.collidepoint(mouse) and self.active:
            self.color = RED
        else:
            self.color = self.default_color
        self.object = self.font.render(self.text, True, self.color)

class Text_Box():
    def __init__(self,center,dimensions,field=''):
        self.rect = pygame.Rect(center[0] - dimensions[0]//2, center[1] - dimensions[1]//2, dimensions[0], dimensions[1])
        self.color_inactive = BLACK
        self.color_active = RED
        self.color = self.color_inactive
        self.field = field
        self.text = self.field
        self.text_color = GREY
        self.font = pygame.font.Font(os.path.join(PATH,"fonts","Folks-Bold.ttf"),int(self.rect.height//1.1))
        self.object = self.font.render(self.text, True, self.text_color)
        self.active = False
        self.start = True
        self.original_width = self.rect.width

    def mouse_event(self,pos):
        if self.rect.collidepoint(pos):
            self.active = True
            if self.start == True:
                self.start = False
                self.text = ""
                self.text_color = BLACK
        else:
            self.active = False
            if self.text == "":
                self.start = True
                self.text_color = GREY
                self.text = self.field
        if self.active:
            self.color = self.color_active
        else:
            self.color = self.color_inactive

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
            self.color = self.color_active
        elif not self.active:
            self.color = self.color_inactive
        self.object = self.font.render(self.text, True, self.text_color)

    def draw(self):
        screen.blit(self.object, (self.rect.x + 5, self.rect.y + 5))
        pygame.draw.rect(screen, self.color, self.rect, 4)

def space_buttons(button_list):
    button_height = sum([i.rect.h for i in button_list])//len(button_list)
    distance = (SIZE[1] - sum([i.rect.h for i in button_list]))//len(button_list)+1
    if len(button_list) % 2 == 0:
        y_pos = SIZE[1]//2 - distance//2
        for i in range(len(button_list)//2-1,-1,-1):
            button_list[i].rect.bottom = y_pos
            y_pos -= distance + height
        y_pos = SIZE[1]//2 + distance//2
        for i in range(len(button_list)//2,len(button_list)):  #change to list slice
            button_list[i].rect.top = y_pos
            y_pos += distance + height
    else:
        y_pos = SIZE[1]//2
        button_list[len(button_list)//2].rect.centery = y_pos
        y_pos -= height//2 + distance
        for button in button_list[len(button_list)//2-1::-1]:
            button.rect.bottom = y_pos
            y_pos -= distance + height
        y_pos = SIZE[1]//2 + height//2 + distance
        for button in button_list[len(button_list)//2+1:]:
            #finish here

def main_menu(window,surface):
    global SIZE,screen
    SIZE = window
    screen = surface
    choice = False
    button_size = 90
    button_list = []
    button_list.append(Button(SIZE[1]//2 - button_size*3,button_size,'Single Player','single',True))
    button_list.append(Button(SIZE[1]//2 - button_size,button_size,'Two Player','double',True))
    button_list.append(Button(SIZE[1]//2,button_size,'AI Player','computer',True))
    button_list.append(Button(SIZE[1]//2 + button_size,button_size,'Watch it Learn','learn',True))
    button_list.append(Button(SIZE[1]//2 + button_size*3,button_size,'Leader Board','leaderboard',True))
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

def game_over_single(window,surface):
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

def pause_menu(window,surface):
    pass

def game_over_double(window,surface):
    pass

def scroll(distance,*lists):
    for list in lists:
        for item in list:
            item.rect.y -= distance

def leaderboard(window,surface):
    global SIZE,screen
    SIZE = window
    screen = surface
    choice = False
    button_size = 90
    try:
        users = json.load(open(os.path.join(PATH,"users.json"),"rt"))
        users = sorted(users,key=lambda i:i[1])
    except FileNotFoundError:
        users = []

    button_list = [Button(button_size,button_size,'Leader Board      High Score','single',False,(0, 45, 179))]
    y_pos = button_list[0].rect.centery
    for user in users:
        y_pos += button_size + 40
        button_list.append(Button(y_pos,button_size,user[0]+"      "+str(user[1]),'single',False))

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
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    for button in button_list:                      
                        if button.rect.collidepoint(mouse) and button.active:
                            return button.action
                elif event.button == 4 and button_list[-1].rect.bottom < SIZE[1] - 30:
                    scroll(-10,button_list)
                elif event.button == 5 and button_list[0].rect.top > 30:
                    scroll(10,button_list)

        pygame.display.flip()       
        clock.tick(60)

if __name__ == "__main__":
    os.environ['SDL_VIDEO_CENTERED'] = '1'
    pygame.init()
    infoObject = pygame.display.Info()
    SIZE = (infoObject.current_w, infoObject.current_h - 30)
    screen = pygame.display.set_mode(SIZE,pygame.RESIZABLE)
    pygame.display.set_caption("NEAT-JUMP")
    leaderboard(SIZE,screen)
