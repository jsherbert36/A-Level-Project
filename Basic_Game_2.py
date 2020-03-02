import math,pygame,random
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
PATH = sys.path[0]

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.width = 20
        #Logo = pygame.image.load(os.path.join(SCRIPT_PATH,"images","logo.bmp")).convert()
        #Logo = pygame.transform.smoothscale(Logo, (550,293))
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
        if self.rect.x > size[0] - self.width + 10:
            self.rect.x = 1
        elif self.rect.x < 0:
            self.rect.x = size[0] - self.width
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
        self.position = position
        self.block_width = block_width
        self.image = pygame.Surface([self.block_width,20])
        self.image.fill(WHITE)
        self.rect = self.image.get_rect()
        self.rect.x = self.position[0]
        self.rect.y = self.position[1]
    def update(self):
        pass

class SideBlock(Block):
    def __init__(self,position,block_width):
        super().__init__(position,block_width)
        self.direction = random.choice(['left','right'])
        self.distance = 120
        if self.position[0] > size[0] - self.distance - self.block_width:
            self.position[0] = size[0] - self.distance - self.block_width
        elif self.position[0] < self.distance - block_width//2:
            self.position[0] = self.distance - block_width//2
    def update(self):
        if self.rect.centerx > self.position[0] + self.distance:
            self.direction = 'left'
        elif self.rect.centerx < self.position[0] - self.distance:
            self.direction = 'right'
        if self.direction == 'left':
            self.rect.x -= 2
        elif self.direction == 'right':
            self.rect.x += 2


class VerticalBlock(Block):
    def __init__(self,position,block_width,distance):
        super().__init__(position,block_width)
        self.direction = random.choice(['up','down'])
        self.distance = distance
        
    def update(self):
        if self.rect.centery < self.position[1] - self.distance:
            self.direction = 'down'
        elif self.rect.centery > self.position[1] + self.distance:
            self.direction = 'up'
        if self.direction == 'up':
            self.rect.y -= 1
        elif self.direction == 'down':
            self.rect.y += 1

        
        
class Alien():
    pass

def move(direction,block_y,sprite_group):
    for sprite in sprite_group:
        sprite.rect.y += direction
        if isinstance(sprite,VerticalBlock):
            sprite.position[1] += direction 
    block_y += direction
    return block_y
    
    
def gameplay():
    all_sprites_group = pygame.sprite.Group()
    player_group = pygame.sprite.Group()
    block_group = pygame.sprite.Group()
    player = Player()
    block_width = 80
    vertical_distance = 60
    block_y = size[1] - 20
    block_x = random.randint(80,size[0] - 80)
    start_block = Block([0,block_y],size[0])
    block_group.add(start_block)
    all_sprites_group.add(start_block)
    while block_y > 70:
        block_y -= random.randint(50,100)
        block_x = (block_x + (random.randint(-350,350))) % (size[0] - block_width)
        new_block = Block([block_x,block_y], block_width)
        block_group.add(new_block)
        all_sprites_group.add(new_block)
        
    player_group.add(player)
    all_sprites_group.add(player)
    game_over = False
    clock = pygame.time.Clock()
    count = 0
    fall = False
    started = False
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
            if block_y > 0:
                block_y -= random.randint(50,100)
                block_x = (block_x + (random.randint(-350,350))) % (size[0] - block_width)
                if block_y < 300:
                    block_type = random.choice(['move','still','still','still','vertical'])
                else:
                    block_type = 'still'
                if block_type == 'move':
                    new_block = SideBlock([block_x,block_y], block_width)
                elif block_type == 'still':
                    new_block = Block([block_x,block_y], block_width)
                elif block_type == 'vertical':
                    block_y -= vertical_distance //2
                    new_block = VerticalBlock([block_x,block_y], block_width, vertical_distance)
                block_group.add(new_block)
                all_sprites_group.add(new_block)
            block_y = move(3,block_y,all_sprites_group)
        if fall == True:
            block_y = move(-15,block_y,all_sprites_group)
        if player.rect.y > size[1] - 300 and start_block.rect.bottom > size[1]:
            fall = True
        else:
            fall = False
        if start_block.rect.y > size[1] + 100:
            started = True
        if player.rect.colliderect(start_block.rect) and started == True:
            game_over = True
            return 'gameover'
        
        
        screen.fill(BLACK)
        all_sprites_group.update()
        player_group.draw(screen)
        block_group.draw(screen)
        pygame.display.flip()

        clock.tick(60)

def gameover():
    font = pygame.font.Font('freesansbold.ttf', 70) 
    exit = False
    clock = pygame.time.Clock()
    while not exit:
        screen.fill(BLACK) 
        Play = font.render('GAME OVER', True, WHITE)
        PlayRect = Play.get_rect()
        PlayRect.center = (size[0]//2, size[1]//2)
        screen.blit(Play, PlayRect) 
        pygame.display.flip()
        for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit = True
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        exit = True
            
        clock.tick(60)


pygame.init()
size = (1280,720)
screen = pygame.display.set_mode(size,pygame.RESIZABLE)
if gameplay() == 'gameover':
    gameover()
else:
    pygame.quit()
