import numpy,math,pygame
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
class Player():
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface([20,20])
        self.image.fill(WHITE)
        self.rect = self.image.get_rect()
        self.direction = 'up'
    def update(self):
        if self.direction == 'up':
            self.rect.y -= speed
        elif self.direction == 'down':
            self.rect.y += speed
        if self.rect.y > 500:
            self.direction = 'up'
        self.change_speed()
    def change_speed(self):
        if self.direction == 'up':
            self.speed -= 1
        elif self.direction == 'down':
            self.speed += 1
        


class Computer(Player):
    pass
class Block():
    pass
class Alien():
    pass
    
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
            player.rect.x += 2
        elif keys[pygame.K_LEFT]:
            player.rect.x -= 2



        screen.fill(BLACK)
        player.update()
        player.draw()
        pygame.display.flip()

        clock.tick(60)


pygame.init()
size = (700,500)
screen = pygame.display.set_mode(size)
gameplay()
pygame.quit()
