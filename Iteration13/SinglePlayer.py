import math,pygame,random,sys,os,json,Menu
from Menu import pause_menu,game_over_single
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
PATH = sys.path[0]

class Player(pygame.sprite.Sprite):
    def __init__(self,x_pos):
        super().__init__()
        self.width = 37
        self.image_list = []
        for i in range(1,9):
            temp_image = pygame.image.load(os.path.join(PATH,"images",("frame-"+str(i)+ ".png"))).convert_alpha()
            self.image_list.append(pygame.transform.smoothscale(temp_image, [self.width + 3, self.width]))
        self.image = self.image_list[0]
        self.image_num = 0
        self.rect = self.image.get_rect()
        self.rect.x = x_pos
        self.rect.y = SIZE[1] - self.width
        self.direction = 'up'
        self.normal_speed = 22
        self.speed = self.normal_speed
        self.terminal_velocity = 24
        self.score = 0

    def update(self):
        self.image_num = (self.image_num + 1 ) % 14
        if self.image_num % 4 == 0:
            self.image = self.image_list[self.image_num//2]
        if self.direction == 'up':
            self.rect.y -= self.speed
        elif self.direction == 'down':
            self.rect.y += self.speed
        self.change_speed()
        if self.rect.right > SIZE[0]:
            self.rect.right = SIZE[0]
        elif self.rect.x < 0:
            self.rect.x = 0
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

    def set_score(self,start_block):
        self.height = start_block.rect.top - self.rect.bottom 
        if self.height > self.score:
            self.score = self.height

    def move(self,direction):
        if direction == 'right':
            self.rect.x += 9
        elif direction == 'left':
            self.rect.x -= 9

    def collision(self,block_group):
        block_hit_list = pygame.sprite.spritecollide(self,block_group,False)
        for block in block_hit_list:
            if self.rect.bottom > block.rect.top and self.direction == 'down':
                self.reverse()
                if block.type == 'onetime':
                    block.hit += 1
        
class Block(pygame.sprite.Sprite):
    def __init__(self,position,block_width):
        super().__init__()
        self.position = position
        self.block_width = block_width
        self.image = pygame.image.load(os.path.join(PATH,"images","Basic_Block.png")).convert()
        self.image = pygame.transform.smoothscale(self.image, [self.block_width, 25])
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = position
        self.type = 'still'
        if random.choice([True,False]) == True:
            self.coin = Coin([self.rect.centerx + random.randint(-10,10),self.rect.y - random.randint(40,100)])
        else:
            self.coin = None

    def update(self):
        pass

class SideBlock(Block):
    def __init__(self,position,block_width):
        super().__init__(position,block_width)
        self.direction = random.choice(['left','right'])
        self.distance = 120
        self.type = 'horizontal'
        if self.position[0] > SIZE[0] - self.distance - self.block_width:
            self.position[0] = SIZE[0] - self.distance - self.block_width
        elif self.position[0] < self.distance + block_width//2:
            self.position[0] = self.distance + block_width//2

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
        self.type = 'vertical'
        
    def update(self):
        if self.rect.centery < self.position[1] - self.distance:
            self.direction = 'down'
        elif self.rect.centery > self.position[1] + self.distance:
            self.direction = 'up'
        if self.direction == 'up':
            self.rect.y -= 1
        elif self.direction == 'down':
            self.rect.y += 1

class OneTimeBlock(Block):
    def __init__(self,position,block_width):
        super().__init__(position,block_width)
        self.type = 'onetime'
        self.hit = 0
        self.image = pygame.image.load(os.path.join(PATH,"images","OneTime_Block.png")).convert()
        self.image = pygame.transform.smoothscale(self.image, [self.block_width, 20])

    def update(self):
        pass

class Coin(pygame.sprite.Sprite):
    def __init__(self,position):
        super().__init__()
        self.block_width = 33
        self.image = pygame.image.load(os.path.join(PATH,"images","coin.png")).convert_alpha()
        self.image = pygame.transform.smoothscale(self.image, [self.block_width, self.block_width])
        self.rect = self.image.get_rect()
        self.rect.centerx, self.rect.y = position

    def update(self):
        pass
        
def move(direction,block_y,sprite_group):
    for sprite in sprite_group:
        sprite.rect.y += direction
        if isinstance(sprite,VerticalBlock):
            sprite.position[1] += direction 
    block_y += direction
    return block_y

def set_block(block_x,block_y,block_width,tolerance):
    block_y -= random.randint(150,160)
    far_left = block_x - block_width//2
    far_right = SIZE[0]- block_x - block_width
    block_x += random.randint(-1 * min(tolerance,far_left),min(far_right,tolerance))
    return block_x,block_y

def choose_block_type(height):
    if height > 1500 and height < 10000:
        return random.choice(['move','still','still','still','still','vertical','onetime'])
    elif height >= 10000:
        return random.choice(['move','still','still','vertical','onetime'])
    else:
        return 'still'

def gameplay(window,surface):
    global SIZE,screen
    SIZE = window
    screen = surface
    background_image_1 = pygame.image.load(os.path.join(PATH,"images","Background.jpg")).convert()
    background_image_1 = pygame.transform.smoothscale(background_image_1, SIZE)
    all_sprites_group = pygame.sprite.Group()
    block_group = pygame.sprite.Group()
    coin_group = pygame.sprite.Group()
    block_width = 150
    tolerance = 200
    vertical_distance = 60
    block_x,block_y = SIZE[0]//2,SIZE[1] - 50
    new_block = Block([block_x,block_y], block_width)
    start_block = Block([0,SIZE[1]-20],SIZE[0])
    block_group.add(new_block)
    all_sprites_group.add(start_block,new_block)

    while block_y > 70:
        block_x,block_y = set_block(block_x,block_y,block_width,tolerance) 
        new_block = Block([block_x,block_y], block_width)
        block_group.add(new_block)
        if new_block.coin != None:
            coin_group.add(new_block.coin)
       
    all_sprites_group.add(block_group,coin_group)   
    player1 = Player(SIZE[0]//2 - 10)
    all_sprites_group.add(player1)
    game_over = False
    clock = pygame.time.Clock()
    count = 0
    high_score = 0
    max = 0
    score_font = pygame.font.Font("freesansbold.ttf", SIZE[0]//64) 
    
# -------------- Main Program Loop ---------------- #
    while not game_over:
        count += 1
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return 'gameover', []
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return 'gameover', []
                elif event.key == pygame.K_SPACE:
                    pause = pause_menu(SIZE,screen)
                    if pause == "gameover": return 'gameover'
                    elif pause == 'main_menu': return None

        keys = pygame.key.get_pressed()
        if keys[pygame.K_RIGHT]:
            player1.move('right')
        elif keys[pygame.K_LEFT]:
            player1.move('left')

        player1.set_score(start_block)
        player1.collision(block_group)
        if player1.score > high_score:
            high_score = player1.score

        if player1.rect.y < SIZE[1]//3 and block_y > -10:
            block_x,block_y = set_block(block_x,block_y,block_width,tolerance) 
            block_type = choose_block_type(player1.score)
            if block_type == 'move':
                new_block = SideBlock([block_x,block_y], block_width)
            elif block_type == 'still':
                new_block = Block([block_x,block_y], block_width)
            elif block_type == 'vertical':
                block_y -= vertical_distance//2 
                new_block = VerticalBlock([block_x,block_y], block_width, vertical_distance)
                block_y -= vertical_distance//2
                new_block.coin = None
            elif block_type == 'onetime':
                new_block = OneTimeBlock([block_x,block_y], block_width)
            block_group.add(new_block)
            all_sprites_group.add(new_block)
            if new_block.coin != None:
                coin_group.add(new_block.coin)
                all_sprites_group.add(new_block.coin)

        coin_hit_list = pygame.sprite.spritecollide(player1,coin_group,True)
        player1.score += len(coin_hit_list * 800)
        
        if count % 15 == 0:
            block_width = int(round(-60/(1+1.0003**(5000 - high_score)) + 160))

        if count % 13 == 0:
            tolerance = int(round(60/(1+1.0003**(5000 - high_score)) + 190))

        if player1.rect.y < 0:
            block_y = move(15,block_y,all_sprites_group)
        elif player1.rect.y < SIZE[1]//6 and player1.rect.y > 0:
            block_y = move(7,block_y,all_sprites_group)
        elif player1.rect.y < SIZE[1]//3 and player1.rect.y > SIZE[1]//6:
            block_y = move(4,block_y,all_sprites_group)

        for block in block_group:
            if block.rect.y > SIZE[1] + 30:
                block.kill()
            if block.type == 'onetime' and block.hit > 0:
                block.kill()

        if player1.rect.top > SIZE[1]:
            game_over = True
            game_over_single(SIZE,screen,player1.score)
            return None
        
        screen.blit(background_image_1,(0,0))
        all_sprites_group.update()
        screen.blit(player1.image,player1.rect)
        block_group.draw(screen)
        coin_group.draw(screen)
        score1_display = score_font.render("Score: " + str(player1.score), True, BLACK)
        screen.blit(score1_display,(SIZE[0]//20, SIZE[1]//20))
        pygame.display.flip()
        clock.tick(60)

if __name__ == "__main__":
    os.environ['SDL_VIDEO_CENTERED'] = '1'
    pygame.init()
    infoObject = pygame.display.Info()
    SIZE = (infoObject.current_w, infoObject.current_h)
    screen = pygame.display.set_mode(SIZE)
    if gameplay(SIZE,screen) == 'gameover':
        pass
    pygame.quit()
