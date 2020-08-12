import math,pygame,random,sys,os,json
WHITE = (255,255,255)
BLACK = (0,0,0)
RED = (204,0,0)
GREY = (190, 190, 190)
PATH = sys.path[0]

class Button():
    def __init__(self,pos,size,text,action,active,color=BLACK,font_path=os.path.join(PATH,"fonts","Folks-Bold.ttf")):
        self.size = size
        self.font = pygame.font.Font(font_path,self.size)
        self.default_color = color
        self.color = self.default_color
        self.text = text
        self.object = self.font.render(self.text, True, self.color)
        self.rect = self.object.get_rect()
        self.rect.center = pos
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

class BackButton(Button):
    def __init__(self,top,bottom):
        pass


class Text_Box():
    def __init__(self,position,size,field):
        self.rect = pygame.Rect(position[0],position[1],10,size)
        self.color_inactive = BLACK
        self.color_active = RED
        self.color = self.color_inactive
        self.field = field
        self.text = self.field
        self.text_color = GREY
        self.font = pygame.font.Font("freesansbold.ttf",int(self.rect.height//1.1))
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
                self.original_width = self.rect.width
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

    def key_event(self,event):
        if self.active:
            if len(self.text) < 16 and event.key not in [pygame.K_BACKSPACE,pygame.K_SPACE,pygame.K_RETURN]:
                self.text += event.unicode

    def update(self,mouse):
        self.rect.width = max(self.original_width, self.object.get_width() + 10)
        if self.rect.collidepoint(mouse):
            self.color = self.color_active
        elif not self.active:
            self.color = self.color_inactive
        self.object = self.font.render(self.text, True, self.text_color)

    def draw(self):
        screen.blit(self.object, (self.rect.x + 5, self.rect.y + (self.rect.h - int(self.rect.height//1.1))//2))
        pygame.draw.rect(screen, self.color, self.rect, 3)

def space_buttons(button_list,gap=math.inf):
    height = sum([i.rect.h for i in button_list])//len(button_list)
    distance = min(gap,(SIZE[1] - sum([i.rect.h for i in button_list]))//len(button_list)+1)
    if len(button_list) % 2 == 0:
        y_pos = SIZE[1]//2 - distance//2
        for button in button_list[len(button_list)//2-1::-1]:
            button.rect.bottom = y_pos
            y_pos -= distance + height
        y_pos = SIZE[1]//2 + distance//2
        for button in button_list[len(button_list)//2:]:
            button.rect.top = y_pos
            y_pos += distance + height
    else:
        button_list[len(button_list)//2].rect.centery = SIZE[1]//2
        y_pos = SIZE[1]//2 - height//2 - distance
        for button in button_list[len(button_list)//2-1::-1]:
            button.rect.bottom = y_pos
            y_pos -= distance + height
        y_pos = SIZE[1]//2 + height//2 + distance
        for button in button_list[len(button_list)//2+1:]:
            button.rect.top = y_pos
            y_pos += distance + height

def main_menu(window,surface):
    global SIZE,screen
    SIZE = window
    screen = surface
    choice = False
    button_size = 90
    button_list = []
    button_list.append(Button([SIZE[0]//2,0],button_size,'Single Player','single',True))
    button_list.append(Button([SIZE[0]//2,0],button_size,'Two Player','double',True))
    button_list.append(Button([SIZE[0]//2,0],button_size,'AI Player','computer',True))
    button_list.append(Button([SIZE[0]//2,0],button_size,'Watch it Learn','learn',True))
    button_list.append(Button([SIZE[0]//2,0],button_size,'Leader Board','leaderboard',True))
    space_buttons(button_list,50)
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

def game_over_single(window,surface,score):
    global SIZE,screen
    SIZE = window
    screen = surface
    choice = False
    button_size = int(SIZE[0]//28.24)
    button_list = []
    username_box = Text_Box([int(SIZE[0]//1.9),int(SIZE[1]//2.165)],button_size,"Username")
    button = Button([int(SIZE[0]//1.73),int(SIZE[1]//1.509)],button_size,str(score),'',False,font_path="freesansbold.ttf")
    button_list += [username_box,button]
    background_image_1 = pygame.image.load(os.path.join(PATH,"images","Game_Over_Single_1.jpg")).convert()
    background_image_1 = pygame.transform.smoothscale(background_image_1, SIZE)
    clock = pygame.time.Clock()
    backspace = 0
    user_list = json.load(open(os.path.join(PATH,"users.json"),"rt"))

    while not choice:
        mouse = pygame.mouse.get_pos() 
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                choice = True
                return 'gameover'
            elif event.type == pygame.KEYDOWN:               
                if event.key == pygame.K_ESCAPE:
                    choice = True
                    return 'gameover'
                elif event.key == pygame.K_RETURN:
                    choice = True
                    if username_box.text == "":
                        return None
                    elif username_box.text in [i[0] for i in user_list]:
                        index = [i[0] for i in user_list].index(username_box.text)
                        if user_list[index][1] < score:
                            user_list[index][1] = score
                    else:
                        user_list.append([username_box.text,score])
                    f = open(os.path.join(PATH,"users.json"),"wt")        
                    json.dump(user_list, f)
                    f.close()
                    return None
                else:
                    username_box.key_event(event)
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                username_box.mouse_event(mouse)                   
                if button.rect.collidepoint(mouse) and button.active:
                    return button.action
        keys = pygame.key.get_pressed()
        if keys[pygame.K_BACKSPACE]:          
            if username_box.active:
                backspace += 1
                if backspace >= 3:
                    username_box.text = username_box.text[:-1]
                    backspace = 0
        screen.blit(background_image_1,(0,0))              
        button.update(mouse)
        button.draw()
        username_box.update(mouse)
        username_box.draw()
        pygame.display.flip()       
        clock.tick(60)

def pause_menu(window,surface):
    global SIZE,screen
    SIZE = window
    screen = surface
    choice = False
    button_size = 90
    button_list = []
    button_list.append(Button([SIZE[0]//2,0],button_size,'Return to Game','play',True))
    button_list.append(Button([SIZE[0]//2,0],button_size,'Main Menu','main_menu',True))
    button_list.append(Button([SIZE[0]//2,0],button_size,'Exit Game','gameover',True))
    space_buttons(button_list,70)
    background_image_1 = pygame.image.load(os.path.join(PATH,"images","Background1-Blur.jpg")).convert()
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

def game_over_double(window,surface,score):
    global SIZE,screen
    SIZE = window
    screen = surface
    choice = False
    button_size = int(SIZE[0]//28.24)
    button_list = []
    username1_box = Text_Box([int(SIZE[0]//2.2),int(SIZE[1]//2.165)],button_size,"username")
    username2_box = Text_Box([int(SIZE[0]//1.7),int(SIZE[1]//2.165)],button_size,"username")
    button = Button([int(SIZE[0]//1.73),int(SIZE[1]//1.509)],button_size,str(score),'',False,font_path="freesansbold.ttf")
    button_list += [username_box,button]
    background_image_1 = pygame.image.load(os.path.join(PATH,"images","Game_Over_Single_1.jpg")).convert()
    background_image_1 = pygame.transform.smoothscale(background_image_1, SIZE)
    clock = pygame.time.Clock()
    backspace = 0
    user_list = json.load(open(os.path.join(PATH,"users.json"),"rt"))

    while not choice:
        mouse = pygame.mouse.get_pos() 
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                choice = True
                return 'gameover'
            elif event.type == pygame.KEYDOWN:               
                if event.key == pygame.K_ESCAPE:
                    choice = True
                    return 'gameover'
                elif event.key == pygame.K_RETURN:
                    choice = True
                    if username_box.text == "":
                        return None
                    elif username_box.text in [i[0] for i in user_list]:
                        index = [i[0] for i in user_list].index(username_box.text)
                        if user_list[index][1] < score:
                            user_list[index][1] = score
                    else:
                        user_list.append([username_box.text,score])
                    f = open(os.path.join(PATH,"users.json"),"wt")        
                    json.dump(user_list, f)
                    f.close()
                    return None
                else:
                    username_box.key_event(event)
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                username_box.mouse_event(mouse)                   
                if button.rect.collidepoint(mouse) and button.active:
                    return button.action
        keys = pygame.key.get_pressed()
        if keys[pygame.K_BACKSPACE]:          
            if username_box.active:
                backspace += 1
                if backspace >= 3:
                    username_box.text = username_box.text[:-1]
                    backspace = 0
        screen.blit(background_image_1,(0,0))              
        button.update(mouse)
        button.draw()
        username_box.update(mouse)
        username_box.draw()
        pygame.display.flip()       
        clock.tick(60)
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
    button_list = [Button([SIZE[0]//2,button_size],button_size,'Leader Board      High Score','single',False,(0, 45, 179))]
    y_pos = button_list[0].rect.centery
    for user in users:
        y_pos += button_size + 40
        button_list.append(Button([SIZE[0]//2,y_pos],button_size,user[0]+"      "+str(user[1]),'single',False))

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
                elif event.button == 4 and button_list[0].rect.top < 30:
                    scroll(-20,button_list)
                elif event.button == 5 and button_list[-1].rect.bottom > SIZE[1] - 30:
                    scroll(20,button_list)

        pygame.display.flip()       
        clock.tick(60)

if __name__ == "__main__":
    os.environ['SDL_VIDEO_CENTERED'] = '1'
    pygame.init()
    infoObject = pygame.display.Info()
    SIZE = (infoObject.current_w, infoObject.current_h - 30)
    screen = pygame.display.set_mode(SIZE,pygame.RESIZABLE)
    pygame.display.set_caption("NEAT-JUMP")
    game_over_single(SIZE,screen,0)
