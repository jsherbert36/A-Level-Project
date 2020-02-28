import math,pygame,random
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.width = 20
        self.image = pygame.Surface([self.width,self.width])
        self.image.fill(WHITE)
        self.rect = self.image.get_rect()
        self.rect.x = size[0]//2
        self.rect.y = size[1] - self.width
        self.direction = 'up'
        self.normal_speed = 20
        self.speed = self.normal_speed
        self.terminal_velocity = 22
    def update(self):
        if self.direction == 'up':
            self.rect.y -= self.speed
        elif self.direction == 'down':
            self.rect.y += self.speed
        self.change_speed()
        if self.rect.x > size[0] - self.width:
            self.rect.x = size[0] - self.width
        elif self.rect.x < 1:
            self.rect.x = 1
        if self.speed > self.terminal_velocity:
            self.speed = self.terminal_velocity
    def change_speed(self):
        if self.speed == 0:
            self.reverse()
        if self.direction == 'up':
            self.speed -= 1
        elif self.direction == 'down':
            self.speed += 1
    def reverse(self):
        if self.direction == 'up':
            self.direction = 'down'
        elif self.direction == 'down':
            self.direction = 'up'
            self.speed = self.normal_speed
        
            
class Computer(Player):
    pass
class Block(pygame.sprite.Sprite):
    def __init__(self,position,block_width):
        super().__init__()
        self.block_width = block_width
        self.image = pygame.Surface([self.block_width,20])
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
    block_width = 80
    block_y = size[1] - 20
    block_x = random.randint(80,size[0] - 80)
    start_block = Block([0,block_y],size[0])
    block_group.add(start_block)
    all_sprites_group.add(start_block)
    while block_y > 70:
        block_y -= random.randint(50,100)
        block_x += random.randint(-1 * min((block_x - 100),550),min(550,size[0] - block_x - 100))
        new_block = Block([block_x,block_y],block_width)
        block_group.add(new_block)
        all_sprites_group.add(new_block)
        
    player_group.add(player)
    all_sprites_group.add(player)
    game_over = False
    clock = pygame.time.Clock()
    count = 0
    fall = False
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
            player.rect.x += 9
        elif keys[pygame.K_LEFT]:
            player.rect.x -= 9
        block_hit_list = pygame.sprite.spritecollide(player,block_group,False)
        for block in block_hit_list:
            fall = False
            if player.rect.bottom > block.rect.top and player.direction == 'down':
                player.reverse()
                count += 1
        if player.rect.y < 200 :
            block_y -= random.randint(50,100)
            block_x += random.randint(-1 * min((block_x - 100),400),min(400,size[0] - block_x - 100))
            new_block = Block([block_x,block_y],block_width)
            block_group.add(new_block)
            all_sprites_group.add(new_block)
            for sprite in all_sprites_group:
                sprite.rect.y += 3
        if fall == True:
            for sprite in all_sprites_group:
                sprite.rect.y -= 10
        if player.rect.y > size[1] - 20 and start_block.rect.y > size[1]:
            fall = True
        if player.rect.bottom > start_block.rect.top:
            start_block.rect.y = size[1] - 20

        screen.fill(BLACK)
        player.update()
        player_group.draw(screen)
        block_group.draw(screen)
        pygame.display.flip()

        clock.tick(60)


pygame.init()
size = (1280,720)
screen = pygame.display.set_mode(size,pygame.RESIZABLE)
gameplay()
pygame.quit()
