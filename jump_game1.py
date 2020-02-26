import numpy,math,pygame

class Player():
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface([20,20])
        self.image.fill(WHITE)
        self.rect = self.image.get_rect()
        self.direction = 'up'
    def update(self):
        if direction == 'up':
            self.rect.y -= speed
        elif direction == 'down':
            self.rect.y += speed
        self.change_speed()
    def change_speed(self):
        
        


class Computer(Player):

class Block():

class Alien():


    
def gameplay():
    player = Player()

    game_over = False
    clock = pygame.time.Clock()

# -------------- Main Program Loop ---------------- #
    while not game_over:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    game_over = True


        keys = pygame.key.get_pressed()
        if keys[pygame.K_RIGHT]:
            player.move('right')
        elif keys[pygame.K_LEFT]:
            player.move('left')



        screen.fill(BLACK)

        pygame.display.flip()

        clock.tick(60)

        
