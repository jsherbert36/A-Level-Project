import math,pygame,random,sys,os,GameOver
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
PATH = sys.path[0]

class Player(pygame.sprite.Sprite):
    def __init__(self,x_pos,second = False):
        super().__init__()
        self.width = 36
        self.image_list = []
        self.second = second
        for i in range(1,9):
            if self.second:
                temp_image = pygame.image.load(os.path.join(PATH,"images",("2frame-"+str(i)+ ".png"))).convert_alpha()
            else:
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
        if self.second:
            if self.rect.right > SIZE[0]:
                self.rect.right = SIZE[0]
            elif self.rect.x < SIZE[0]//2:
                self.rect.x = SIZE[0]//2
        else:
            if self.rect.right > SIZE[0]//2:
                self.rect.right = SIZE[0]//2
            elif self.rect.x < 0:
                self.rect.x = 0
        if self.speed > self.terminal_velocity and self.direction == "down":
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
        self.coin = Coin([self.rect.centerx + random.randint(-10,10),self.rect.y - random.randint(40,100)])

    def update(self):
        pass

class SideBlock(Block):
    def __init__(self,position,block_width):
        super().__init__(position,block_width)
        self.direction = random.choice(['left','right'])
        self.distance = 120
        self.type = 'horizontal'
        if position[0] < SIZE[0]//2:
            if self.position[0] > SIZE[0]//2 - self.distance - self.block_width:
                self.position[0] = SIZE[0]//2 - self.distance - self.block_width
            elif self.position[0] < self.distance + self.block_width//2:
                self.position[0] = self.distance + self.block_width//2
        else:
            if self.position[0] > SIZE[0] - self.distance - self.block_width:
                self.position[0] = SIZE[0] - self.distance - self.block_width
            elif self.position[0] < SIZE[0]//2 + self.distance + self.block_width//2:
                self.position[0] = SIZE[0]//2 + self.distance + self.block_width//2

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

def move(direction,block_y,sprite_group,player):
    for sprite in sprite_group:
        if (player == 1 and sprite.rect.x < SIZE[0]//2) or (player == 2 and sprite.rect.x > SIZE[0]//2):
            sprite.rect.y += direction
            if isinstance(sprite,VerticalBlock):
                sprite.position[1] += direction 
    if player == 1:
        block_y[0] += direction
    else: 
        block_y[1] += direction
    return block_y

def set_block(block_x,block_y,block_width,tolerance):
    temp_y = random.randint(150,160)
    block_y = list(map(lambda x:x - temp_y, block_y))
    far_left = block_x - block_width
    far_right = SIZE[0]- block_x - block_width*2
    block_x += random.randint(-1 * min(tolerance*2,far_left),min(far_right,tolerance*2))
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
    background_image_1 = pygame.image.load(os.path.join(PATH,"images","Background2.jpg")).convert()
    background_image_1 = pygame.transform.smoothscale(background_image_1, SIZE)
    all_sprites_group = pygame.sprite.Group()
    player_list = []
    block_group_list = [pygame.sprite.Group(),pygame.sprite.Group()]
    coin_group = pygame.sprite.Group()
    block_width = 150
    tolerance = 200
    vertical_distance = 60
    block_x = SIZE[0]//2
    block_y = [SIZE[1] - 50,SIZE[1] - 50]
    new_block = [Block([block_x//2,block_y[0]], block_width),Block([block_x//2 +SIZE[0]//2,block_y[1]], block_width)]
    start_block = Block([0,SIZE[1]-20],SIZE[0])
    block_group_list[0].add(new_block[0])
    block_group_list[1].add(new_block[1])
    all_sprites_group.add(start_block,new_block)

    while max(block_y) > 70:
        block_x,block_y = set_block(block_x,block_y,block_width,tolerance) 
        new_block1 = Block([block_x//2,block_y[0]], block_width)
        new_block2 = Block([block_x//2 +SIZE[0]//2,block_y[1]], block_width)
        block_group_list[0].add(new_block1)
        block_group_list[1].add(new_block2)
        if random.choice([True,False]):
            coin_group.add(new_block1.coin,new_block2.coin)     
    player1 = Player(round(SIZE[0]*0.25))
    player2 = Player(round(SIZE[0]*0.75),True)
    player_list += [player1,player2]
    all_sprites_group.add(player1,player2,coin_group,block_group_list)
    game_over = False
    clock = pygame.time.Clock()
    count = 0
    high_score = 0
    max_score = 0
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

        keys = pygame.key.get_pressed()
        if keys[pygame.K_RIGHT]:
            player2.move('right')
        elif keys[pygame.K_LEFT]:
            player2.move('left')
        if keys[pygame.K_a]:
            player1.move('left')
        elif keys[pygame.K_d]:
            player1.move('right')

        for i,player in enumerate(player_list):
            player.set_score(start_block)
            if player.score > high_score:
                high_score = player.score
                max_score = i
        if player1.alive:
            player1.collision(block_group_list[0])
        if player2.alive:
            player2.collision(block_group_list[1])            
        if max_score >= len(player_list):
            max_score = len(player_list) - 1

        if player_list[max_score].rect.y < SIZE[1]//3 and max(block_y) > -10:
            block_x,block_y = set_block(block_x,block_y,block_width,tolerance) 
            block_type = choose_block_type(player_list[max_score].score)
            if block_type == 'move':
                new_block = [SideBlock([block_x//2,block_y[0]], block_width), SideBlock([block_x//2 + SIZE[0]//2,block_y[1]], block_width)]
            elif block_type == 'still':
                new_block = [Block([block_x//2,block_y[0]], block_width),Block([block_x//2 + SIZE[0]//2,block_y[1]], block_width)]
            elif block_type == 'vertical':
                block_y = list(map(lambda x:x - vertical_distance//2,block_y)) 
                new_block = [VerticalBlock([block_x//2,block_y[0]], block_width, vertical_distance),VerticalBlock([block_x//2+SIZE[0]//2,block_y[1]], block_width, vertical_distance)]
                block_y = list(map(lambda x:x - vertical_distance//2,block_y)) 
                new_block[0].coin = None
                new_block[1].coin = None
            elif block_type == 'onetime':
                new_block = [OneTimeBlock([block_x//2,block_y[0]], block_width),OneTimeBlock([block_x//2+SIZE[0]//2,block_y[1]], block_width)]
            block_group_list[0].add(new_block[0])
            block_group_list[1].add(new_block[1])
            all_sprites_group.add(new_block)
            if random.choice([True,False]) and new_block[0].coin != None:
                coin_group.add(new_block[0].coin,new_block[1].coin)
                all_sprites_group.add(new_block[0].coin,new_block[1].coin)

        coin1_hit_list = pygame.sprite.spritecollide(player_list[0],coin_group,True)
        player_list[0].score += len(coin1_hit_list * 800)
        if len(player_list) > 1:
            coin2_hit_list = pygame.sprite.spritecollide(player_list[1],coin_group,True)
            player_list[1].score += len(coin2_hit_list * 800)
        
        if count % 15 == 0:
            block_width = int(round(-60/(1+1.0003**(5000 - high_score)) + 160))

        if count % 13 == 0:
            tolerance = int(round(60/(1+1.0003**(5000 - high_score)) + 190))
   
        if player1.rect.y < 0:
            block_y = move(11,block_y,all_sprites_group,1)
        elif player1.rect.y < SIZE[1]//6 and player1.rect.y > 0:
            block_y = move(7,block_y,all_sprites_group,1)
        elif player1.rect.y < SIZE[1]//3 and player1.rect.y > SIZE[1]//6:
            block_y = move(4,block_y,all_sprites_group,1)

        if player2.rect.y < 0:
            block_y = move(11,block_y,all_sprites_group,2)
        elif player2.rect.y < SIZE[1]//6 and player2.rect.y > 0:
            block_y = move(7,block_y,all_sprites_group,2)
        elif player2.rect.y < SIZE[1]//3 and player2.rect.y > SIZE[1]//6:
            block_y = move(4,block_y,all_sprites_group,2)

        for block_group in block_group_list:
            for block in block_group:
                if block.rect.y > SIZE[1] + 30 or (block.type == "onetime" and block.hit > 0):
                    block.kill()
        
        for player in player_list:
            if player.rect.top > SIZE[1]:
                    player_list.pop(player_list.index(player))
                    player.kill()

        if not player_list:
            game_over = True
            return 'lost',[player1.score,player2.score]
        
        screen.blit(background_image_1,(0,0))
        all_sprites_group.update()
        if player1.alive:
            screen.blit(player1.image,player1.rect)
        if player2.alive:
            screen.blit(player2.image,player2.rect)
        block_group_list[0].draw(screen)
        block_group_list[1].draw(screen)
        coin_group.draw(screen)
        screen.blit(score_font.render("Player 1 Score: " + str(player1.score), True, BLACK),(SIZE[0]//20, SIZE[1]//20))
        screen.blit(score_font.render("Player 2 Score: " + str(player2.score), True, BLACK),(SIZE[0]//20 + SIZE[0]//2, SIZE[1]//20))
        pygame.display.flip()
        clock.tick(60)

if __name__ == "__main__":
    os.environ['SDL_VIDEO_CENTERED'] = '1'
    pygame.init()
    infoObject = pygame.display.Info()
    SIZE = (infoObject.current_w, infoObject.current_h - 50)
    print(SIZE[1])
    screen = pygame.display.set_mode(SIZE,pygame.RESIZABLE)
    if gameplay(SIZE,screen) == 'gameover':
        pass
    pygame.quit()
