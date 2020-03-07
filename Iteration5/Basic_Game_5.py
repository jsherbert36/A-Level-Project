import math,pygame,random,sys,os,time,neat,numpy
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
PATH = sys.path[0]

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.width = 40
        self.image_list = []
        for i in range(1,9):
            temp_image = pygame.image.load(os.path.join(PATH,"images",("frame-"+str(i)+ ".png"))).convert()
            temp_image.set_colorkey(BLACK)
            self.image_list.append(pygame.transform.smoothscale(temp_image, [self.width, self.width]))
        self.image = self.image_list[0]
        self.image_num = 0
        self.rect = self.image.get_rect()
        self.rect.x = numpy.random.randint(0,size[0])
        self.rect.y = size[1] - self.width
        self.direction = 'up'
        self.normal_speed = 20
        self.speed = self.normal_speed
        self.terminal_velocity = 22
        self.height = 0
        self.score = 0
        self.current_block = 0
        self.current_pos = [size[0]//2,size[1] - 20]
        self.horizontal_direction = 'none'
        self.alive = True

    def update(self):
        self.image_num = (self.image_num + 1 ) % 14
        if self.image_num % 3 == 0:
            self.image = self.image_list[self.image_num//2]
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

    def collision(self,block_group,start_block):
        block_hit_list = pygame.sprite.spritecollide(self,block_group,False)
        for block in block_hit_list:
            if self.rect.bottom > block.rect.top and self.direction == 'down':
                self.current_block = block.number
                self.current_pos = block.rect.center
                self.reverse()
        if self.rect.colliderect(start_block):
            if self.rect.bottom > start_block.rect.top and self.direction == 'down':
                self.reverse()

    def set_score(self,start_block):
        self.height = start_block.rect.top - self.rect.bottom 
        if self.height > self.score:
            self.score = self.height
        
    def set_next(self,block_group):
        for block in block_group:
            if block.number == self.current_block + 1:
                self.next_pos = block.rect.topleft

    def think(self,size,block_width):
        if abs(self.next_pos[0] - self.rect.centerx) > size[0]//2:
            if self.rect.centerx < self.next_pos[0]:
                self.temp_direction = 'left'
            elif self.rect.centerx > self.next_pos[0]:
                self.temp_direction = 'right'
            else: 
                self.temp_direction = 'none'
        elif self.rect.centerx < self.next_pos[0]:
            self.temp_direction = 'right'
        elif self.rect.centerx > self.next_pos[0] + block_width:
            self.temp_direction = 'left'
        else:
            self.temp_direction = 'none'
        if self.horizontal_direction == 'none':
            if self.current_pos[1] - self.rect.y > 40 and self.direction == 'up':
                self.horizontal_direction = self.temp_direction
            else: 
                self.horizontal_direction = 'none'
        else:
            self.horizontal_direction = self.temp_direction

    def move(self):
        if self.horizontal_direction == 'right':
            self.rect.x += 9
        elif self.horizontal_direction == 'left':
            self.rect.x -= 9
    
class Block(pygame.sprite.Sprite):
    def __init__(self,position,block_width,number):
        super().__init__()
        self.number = number
        self.position = position
        self.block_width = block_width
        self.image = pygame.image.load(os.path.join(PATH,"images","Basic_Block.png")).convert()
        self.image = pygame.transform.smoothscale(self.image, [self.block_width, 20])
        self.rect = self.image.get_rect()
        self.rect.x = self.position[0]
        self.rect.y = self.position[1]
        self.alive = True


def move(direction,block_y,block_list,player_list,start_block):
    for block in block_list:
        if block.alive == True:
            block.rect.y += direction
    for player in player_list:
        if block.alive == True:
            player.rect.y += direction
    start_block.rect.y += direction
    block_y += direction
    return block_y
    
    
def gameplay():
    POPULATION_SIZE = 40
    score_font = pygame.font.Font("freesansbold.ttf", 35) 
    player_list = []
    block_list = []
    block_count = 0
    for i in range(POPULATION_SIZE):
        new_player = Player()
        player_list.append(new_player)
    block_width = 90
    block_y = size[1] - 20
    block_x = random.randint(80,size[0] - 80)
    start_block = Block([0,block_y],size[0],block_count)
    block_count += 1
    while block_y > 70:
        block_y -= random.randint(50,100)
        block_x = (block_x + (random.randint(-325,325))) % (size[0] - block_width)
        new_block = Block([block_x,block_y], block_width,block_count)
        block_count += 1
        block_list.append(new_block)   
    game_over = False
    clock = pygame.time.Clock()
    horizontal_direction = 'none'
    max_score = 0
    max_index = 0
    
# -------------- Main Program Loop ---------------- #
    while not game_over:
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
                pygame.quit()
                return 'exit'
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    game_over = True
                    return 'gameover'

            max_score = 0

        for player in player_list:
            if player.alive == True:
                player.set_score(start_block)
                player.set_next(block_list) 
                player.think(size,block_width)
                player.move()
                player.collision(block_list,start_block)
                if player.score > max_score:
                    max_score = player.score
                    max_index = player_list.index(player)

        if player_list[max_index].rect.y < size[0]//4 :            
            if block_y > 0:
                temp_y = random.randint(50,100)
                block_y -= temp_y
                block_x = (block_x + (random.randint(-340,340))) % (size[0] - block_width)
                new_block = Block([block_x,block_y], block_width,block_count)
                block_count += 1
                block_list.append(new_block)
            block_y = move(4,block_y,block_list,player_list,start_block)
            
        for i in range(len(block_list)):
            if block_list[i].rect.y > size[1] + 50:
                block_list[i].alive = False

        for i in range(len(player_list)):
            if player_list[i].rect.bottom > size[1]:
                player_list[i].alive = False
        
        if all(player.alive == False for player in player_list):
            game_over = True
            return 'gameover'

        screen.blit(background_image_1,(0,0))     
        
        for block in block_list:
            if block.alive == True:
                block.update
                screen.blit(block.image,block.rect)
        for player in player_list:
            if player.alive == True:
                player.update()
                screen.blit(player.image,player.rect)
        
        score_display = score_font.render(str(max_score), True, BLACK)
        screen.blit(score_display,(size[0]//20, size[1]//20))

        pygame.display.flip()
        clock.tick(60)

if __name__ == '__main__':
    pygame.init()
    size = (1280,720)
    screen = pygame.display.set_mode(size)
    background_image_1 = pygame.image.load(os.path.join(PATH,"images","Background.jpg")).convert()
    background_image_1 = pygame.transform.smoothscale(background_image_1, size)
    while True:
        if gameplay() != 'gameover':
            break

