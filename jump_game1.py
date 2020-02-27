import numpy,math,pygame
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface([20,20])
        self.image.fill(WHITE)
        self.rect = self.image.get_rect()
        self.rect.x = size[0]//2
        self.rect.y = size[1] - 20
        self.direction = 'up'
        self.speed = 20
        self.terminal_velocity = 23
    def update(self):
        if self.direction == 'up':
            self.rect.y -= self.speed
        elif self.direction == 'down':
            self.rect.y += self.speed
        if self.rect.y > 480:
            self.reverse()
            self.rect.y = 480
        self.change_speed()
    def change_speed(self):
        if self.speed == 0:
            self.reverse
        if self.direction == 'up':
            self.speed -= 1
        elif self.direction == 'down':
            self.speed += 1
    def reverse(self):
        print(self.speed)
        if self.direction == 'up':
            self.direction = 'down'
        elif self.direction == 'down':
            self.direction = 'up'
            if self.speed < 18
        if self.speed > self.terminal_velocity:
            self.speed = self.terminal_velocity
            
class Computer(Player):
    pass
class Block(pygame.sprite.Sprite):
    def __init__(self,position):
        super().__init__()
        self.image = pygame.Surface([80,20])
        self.image.fill(WHITE)
        self.rect = self.image.get_rect()
        self.rect.x = position[0]
        self.rect.y = position[1]
        
   
class Alien():
    pass
    
def gameplay():
    all_sprites_group = pygame.sprite.Group()
    player_group = pygame.sprite.Group()
    block_group = pygame.sprite.Group()
    player = Player()
    test_block = Block([size[0]//2,400])
    block_group.add(test_block)
    player_group.add(player)
    all_sprites_group.add(player,test_block)
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
            player.rect.x += 5
        elif keys[pygame.K_LEFT]:
            player.rect.x -= 5
        if pygame.sprite.spritecollide(player,block_group,False):
            player.reverse()

        screen.fill(BLACK)
        player.update()
        player_group.draw(screen)
        block_group.draw(screen)
        pygame.display.flip()

        clock.tick(60)


pygame.init()
size = (700,500)
screen = pygame.display.set_mode(size)
gameplay()
pygame.quit()
