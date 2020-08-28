import math,pygame,random,sys,os,json
WHITE = (255,255,255)
BLACK = (0,0,0)
RED = (204,0,0)
GREY = (190, 190, 190)
PATH = sys.path[0]

class Button():
    def __init__(self,pos,size,text,action,active,color=BLACK,font_path=os.path.join(PATH,"fonts","SF-UI-Display-Bold.otf"),left_justified = False):
        self.size = size
        self.font = pygame.font.Font(font_path,self.size)
        self.default_color = color
        self.color = self.default_color
        self.text = text
        self.object = self.font.render(self.text, True, self.color)
        self.rect = self.object.get_rect()
        self.rect.center = pos
        if left_justified:
            self.rect.midleft = pos
        self.action = action
        self.active = active
        if self.active:
            self.default_color = GREY
            self.image_list = [pygame.image.load(os.path.join(PATH,"images","Button1_Left.png")).convert_alpha(),
                               pygame.image.load(os.path.join(PATH,"images","Button1_Center.png")).convert_alpha(),
                               pygame.image.load(os.path.join(PATH,"images","Button1_Right.png")).convert_alpha()]
            self.image_list = [pygame.transform.smoothscale(self.image_list[0], [int((self.rect.height + 10)//1.9), self.rect.height + SIZE[1]//72]),
                               pygame.transform.smoothscale(self.image_list[1], [self.rect.width, self.rect.height + SIZE[1]//72]),
                               pygame.transform.smoothscale(self.image_list[2], [int((self.rect.height + 10)//1.9), self.rect.height + SIZE[1]//72])]
            self.image_rect_list = [self.image_list[0].get_rect(),
                                    self.image_list[1].get_rect(),
                                    self.image_list[2].get_rect()]
            self.image_rect_list[1].center = self.rect.center
            self.image_rect_list[0].midright = self.rect.midleft
            self.image_rect_list[2].midleft = self.rect.midright

    def draw(self):
        if self.active:
            for image,rect in zip(self.image_list,self.image_rect_list):
                screen.blit(image,rect)
        screen.blit(self.object,self.rect)

    def update(self,mouse):
        if self.rect.collidepoint(mouse) and self.active:
            self.color = WHITE
        else:
            self.color = self.default_color
        self.object = self.font.render(self.text, True, self.color)

class BackButton(Button):
    def __init__(self,position,text="Back"):
        if position == "topright":
            self.pos = [SIZE[0]-(SIZE[0]//20),SIZE[1]//18]
        elif position == "bottomright":
            self.pos = [SIZE[0]-(SIZE[0]//20),SIZE[1]-(SIZE[1]//18)]
        elif position == "topleft":
            self.pos = [SIZE[0]//20,SIZE[1]//18]
        elif position == "bottomleft":
            self.pos = [SIZE[0]//20,SIZE[1]-(SIZE[1]//18)]
        super().__init__(self.pos,SIZE[0]//53,text,"back",True)

class Text_Box():
    def __init__(self,position,size,width,left_justified=False):
        self.rect = pygame.Rect(0,0,width,size)
        self.width = width
        self.rect.center = position
        if left_justified:
            self.rect.midleft = position
        self.text = ""
        self.color = BLACK
        self.font = pygame.font.Font(os.path.join(PATH,"fonts","SF-UI-Display-Bold.otf"),int(self.rect.height//1.12))
        self.object = self.font.render(self.text, True,BLACK)
        self.text_rect = self.object.get_rect()
        self.active = True
        self.blink = True
        self.blink_timer = 0.0

    def mouse_event(self,pos):
        if self.rect.collidepoint(pos):
            self.active = True
        else: 
            self.active = False  

    def key_event(self,event):
        if self.active and len(self.text) < 12 and event.key not in [pygame.K_BACKSPACE,pygame.K_SPACE,pygame.K_RETURN]:
            self.text += event.unicode

    def update(self,mouse):
        self.rect.width = max(self.width, self.text_rect.width + 20)
        self.object = self.font.render(self.text,True,BLACK)
        self.text_rect = self.object.get_rect()
        self.text_rect.midleft = [self.rect.x + 10,self.rect.centery]
        if pygame.time.get_ticks()-self.blink_timer > 300:
            self.blink = not self.blink
            self.blink_timer = pygame.time.get_ticks()
        if self.active:
            self.color = RED
        else:
            self.color = BLACK

    def draw(self):
        pygame.draw.rect(screen,WHITE,self.rect)
        pygame.draw.rect(screen, self.color, self.rect, 3)
        screen.blit(self.object,self.text_rect)
        if self.blink and self.active:
            pygame.draw.rect(screen,BLACK,pygame.Rect(self.text_rect.right,self.rect.y + 6,4,self.rect.h - 12))

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
    for button in button_list:
        if button.active:
            button.image_rect_list[1].center = button.rect.center
            button.image_rect_list[0].midright = button.rect.midleft
            button.image_rect_list[2].midleft = button.rect.midright

def main_menu(window,surface):
    global SIZE,screen
    SIZE = window
    screen = surface
    choice = False
    button_size = 60
    button_list = []
    button_list.append(Button([SIZE[0]//2,0],button_size,'Single Player','single',True))
    button_list.append(Button([SIZE[0]//2,0],button_size,'Two Player','double',True))
    button_list.append(Button([SIZE[0]//2,0],button_size,'AI Player','computer',True))
    button_list.append(Button([SIZE[0]//2,0],button_size,'Watch it Learn','learn',True))
    button_list.append(Button([SIZE[0]//2,0],button_size,'Leader Board','leaderboard',True))
    space_buttons(button_list,SIZE[1]//10)
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

def game_over_single(window,surface,score):
    global SIZE,screen
    SIZE = window
    screen = surface
    choice = False
    button_size = SIZE[1]//15
    username_box = Text_Box([int(SIZE[0]//1.9),int(SIZE[1]//2.165)],button_size,200,left_justified=True)
    button_list = [username_box]
    button_list += [Button([int(SIZE[0]//1.9),int(SIZE[1]//2.165)+button_size*2],button_size,str(score),'',False,left_justified=True),
                    Button([SIZE[0]//3,int(SIZE[1]//2.165)],button_size,"Username:",'',False,left_justified=True),
                    Button([SIZE[0]//3,int(SIZE[1]//2.165)+button_size*2],button_size,"Score:",'',False,left_justified=True),
                    Button([SIZE[0]//2,SIZE[1]//4],button_size + 20,"Save Your Score:",'',False),
                    BackButton("bottomright",text="Done")]
    background_image_1 = pygame.image.load(os.path.join(PATH,"images","Background1-Blur.jpg")).convert()
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
                    username_box.active = False
                else:
                    username_box.key_event(event)
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                username_box.mouse_event(mouse) 
                if button_list[-1].rect.collidepoint(mouse):
                    if username_box.text in [i[0] for i in user_list] and username_box.text != "":
                        index = [i[0] for i in user_list].index(username_box.text)
                        if user_list[index][1] < score:
                            user_list[index][1] = score
                    elif username_box.text != "":
                        user_list.append([username_box.text,score])
                    f = open(os.path.join(PATH,"users.json"),"wt")        
                    json.dump(user_list, f)
                    f.close()
                    return None
        if pygame.key.get_pressed()[pygame.K_BACKSPACE]:          
            if username_box.active:
                backspace += 1
                if backspace >= 3:
                    username_box.text = username_box.text[:-1]
                    backspace = 0
        screen.blit(background_image_1,(0,0))   
        for button in button_list:
            button.update(mouse)
            button.draw()
        pygame.display.flip()       
        clock.tick(60)

def pause_menu(window,surface):
    global SIZE,screen
    SIZE = window
    screen = surface
    choice = False
    button_size = 60
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
                    elif event.key == pygame.K_SPACE:
                        return 'play'
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
    button_size = SIZE[1]//15
    username_box1 = Text_Box([int(SIZE[0]//3.49),int(SIZE[1]//2.165)],button_size,200,left_justified=True)
    username_box2 = Text_Box([int(SIZE[0]//1.29),int(SIZE[1]//2.165)],button_size,200,left_justified=True)
    button_list = [username_box1,username_box2]
    button_list += [Button([int(SIZE[0]//3.49),int(SIZE[1]//2.165)+button_size*2],button_size,str(score[0]),'',False,left_justified=True),
                    Button([int(SIZE[0]//9.6),int(SIZE[1]//2.165)],button_size,"Username:",'',False,left_justified=True),
                    Button([int(SIZE[0]//9.6),int(SIZE[1]//2.165)+button_size*2],button_size,"Score:",'',False,left_justified=True),
                    Button([SIZE[0]//2,SIZE[1]//6],button_size + 30,"Save Your Score:",'',False),                   
                    Button([int(SIZE[0]//1.29),int(SIZE[1]//2.165)+button_size*2],button_size,str(score[1]),'',False,left_justified=True),
                    Button([int(SIZE[0]//1.83),int(SIZE[1]//2.165)],button_size,"Username:",'',False,left_justified=True),
                    Button([int(SIZE[0]//1.83),int(SIZE[1]//2.165)+button_size*2],button_size,"Score:",'',False,left_justified=True),
                    Button([SIZE[0]//4,SIZE[1]//3],button_size,"Player 1",'',False),
                    Button([int(SIZE[0]//1.33),SIZE[1]//3],button_size,"Player 2",'',False),
                    BackButton("bottomright",text="Done")]
    background_image_1 = pygame.image.load(os.path.join(PATH,"images","Background1-Blur.jpg")).convert()
    background_image_1 = pygame.transform.smoothscale(background_image_1, SIZE)
    clock = pygame.time.Clock()
    backspace = 0
    user_list = json.load(open(os.path.join(PATH,"users.json"),"rt"))
    username_box2.active = False
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
                    username_box1.active = False
                    username_box2.active = False
                else:
                    username_box1.key_event(event)
                    username_box2.key_event(event)
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                username_box1.mouse_event(mouse) 
                username_box2.mouse_event(mouse)
                if button_list[-1].rect.collidepoint(mouse):
                    for j,box in enumerate(button_list[:2]):
                        if box.text in [i[0] for i in user_list] and box.text != "":
                            index = [i[0] for i in user_list].index(box.text)
                            if user_list[index][1] < score[j]:
                                user_list[index][1] = score[j]
                        elif box.text != "":
                            user_list.append([box.text,score[j]])
                    f = open(os.path.join(PATH,"users.json"),"wt")        
                    json.dump(user_list, f)
                    f.close()
                    return None
        if pygame.key.get_pressed()[pygame.K_BACKSPACE]:  
            for box in button_list[:2]:
                if box.active:
                    backspace += 1
                    if backspace >= 3:
                        box.text = box.text[:-1]
                        backspace = 0
        screen.blit(background_image_1,(0,0))   
        for button in button_list:
            button.update(mouse)
            button.draw()
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
    button_size = SIZE[0]//27
    try:
        users = json.load(open(os.path.join(PATH,"users.json"),"rt"))
        users = sorted(users,key=lambda i:i[1],reverse=True)
    except FileNotFoundError:
        users = []
    button_list = [Button([int(SIZE[0]//3.55),button_size],SIZE[0]//24,'User','single',False,(0, 45, 179),left_justified=True),
                   Button([int(SIZE[0]//1.66),button_size],SIZE[0]//24,'High Score','single',False,(0, 45, 179),left_justified=True)]
    y_pos = button_list[0].rect.centery + 10
    for user in users:
        y_pos += button_size + 30
        button_list += [Button([int(SIZE[0]//3.55),y_pos],button_size,user[0],'single',False,left_justified=True),
                        Button([int(SIZE[0]//1.66),y_pos],button_size,str(user[1]),'single',False,left_justified=True)]
    button_list.append(BackButton("topleft"))
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
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    for button in button_list:                      
                        if button.rect.collidepoint(mouse) and button.active:
                            return button.action
                elif event.button == 4 and button_list[0].rect.top < 30:
                    scroll(-25,button_list[:-1])
                elif event.button == 5 and button_list[-2].rect.bottom > SIZE[1] - 30:
                    scroll(25,button_list[:-1])

        pygame.display.flip()       
        clock.tick(60)

if __name__ == "__main__":
    os.environ['SDL_VIDEO_CENTERED'] = '1'
    pygame.init()
    infoObject = pygame.display.Info()
    SIZE = (infoObject.current_w, infoObject.current_h - 30)
    screen = pygame.display.set_mode(SIZE,pygame.RESIZABLE)
    pygame.display.set_caption("NEAT-JUMP")
    game_over_double(SIZE,screen,[0,0])
