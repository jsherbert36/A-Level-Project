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
    button_list = []

    while not game_over and not choice:
        screen.fill(BLACK)  
        mouse = pygame.mouse.get_pos()      
        
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
