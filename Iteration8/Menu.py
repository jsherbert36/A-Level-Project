class Button():
    Button.WHITE = (255,255,255)
    Button.BLACK = (0,0,0)
    Button.RED = (204,0,0)
    def __init__(y_pos,size,text):
        self.size = size
        self.font = pygame.font.Font('freesansbold.ttf',self.size)
        self.colour = Button.WHITE
        self.text = text
        self.object = self.font.render(self.text, True, self.colour)
        self.rect = self.object.get_rect()
        self.rect.x = SIZE[0]//2
        self.rect.y = y_pos

    def draw(self):
        screen.blit(self.object,self.rect)

    def update(self,mouse):
        if self.rect.collidepoint(mouse):
            self.colour = Button.RED
        else:
            self.colour = Button.WHITE
        self.object = self.font.render(self.text, True, self.colour)

def Menu1(window,surface):
    global SIZE,screen
    SIZE = window
    screen = surface
    choice = False
    
    global game_over
    game_over = False
    while not game_over and not choice:
        screen.fill(BLACK) 
        Pong = font.render('NEAT JUMP', True, WHITE)
        PongRect = Pong.get_rect()
        PongRect.center = (CenterX, SIZE[1] // 3) 
        screen.blit(Pong, PongRect) 
        mouse = pygame.mouse.get_pos()      
        Single = font2.render('SINGLEPLAYER', True, SingleColour)
        SingleRect = Single.get_rect()
        SingleRect.center = (CenterX, SIZE[1] // 2) 
        screen.blit(Single, SingleRect) 
        if SingleRect.collidepoint(mouse):    
            SingleColour = RED
        else:
            SingleColour = WHITE  
        Multi = font2.render('MULTIPLAYER', True, MultiColour)
        MultiRect = Multi.get_rect()
        MultiRect.center = (CenterX, int(SIZE[1] // 1.7)) 
        screen.blit(Multi, MultiRect) 
        if MultiRect.collidepoint(mouse):
            MultiColour = RED
        else:
            MultiColour = WHITE
        Score = font2.render('SCOREBOARD', True, ScoreColour)
        ScoreRect = Score.get_rect()
        ScoreRect.center = (CenterX, int(SIZE[1] // 1.46)) 
        screen.blit(Score, ScoreRect) 
        if ScoreRect.collidepoint(mouse):
            ScoreColour = RED
        else:
            ScoreColour = WHITE
        
        Message = font3.render('PRESS ESC TO EXIT', True, WHITE)
        MessageRect = Message.get_rect()
        MessageRect.center = (CenterX, int(SIZE[1]//1.2)) 
        screen.blit(Message, MessageRect) 
        pygame.display.flip()

        for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    game_over = True
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        game_over = True
                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    mouse = pygame.mouse.get_pos()
                    if SingleRect.collidepoint(mouse):
                        choice = True
                        return 'single'
                    elif MultiRect.collidepoint(mouse):
                        choice = True
                        return 'multi'
                    elif ScoreRect.collidepoint(mouse):
                        choice = True
                        return 'score'     
        clock.tick(60)
