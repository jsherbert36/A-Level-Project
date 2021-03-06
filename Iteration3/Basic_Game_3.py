import math,pygame,random,sys,os,time
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
PATH = sys.path[0]
import Test_API

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
        self.rect.x = size[0]//2
        self.rect.y = size[1] - self.width
        self.direction = 'up'
        self.normal_speed = 20
        self.speed = self.normal_speed
        self.terminal_velocity = 22
        self.height = 0
        self.score = 0

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
        
            
class Computer(Player):
    pass

class Block(pygame.sprite.Sprite):
    def __init__(self,position,block_width,number,Type = 'Still'):
        super().__init__()
        self.Type = Type
        self.number = number
        self.position = position
        self.block_width = block_width
        self.image = pygame.image.load(os.path.join(PATH,"images","Basic_Block.png")).convert()
        self.image = pygame.transform.smoothscale(self.image, [self.block_width, 20])
        self.rect = self.image.get_rect()
        self.rect.x = self.position[0]
        self.rect.y = self.position[1]
        self.direction = None
    def update(self):
        pass

class SideBlock(Block):
    def __init__(self,position,block_width,number):
        super().__init__(position,block_width,number,'Horizontal')
        self.direction = random.choice(['left','right'])
        self.distance = 120
        if self.position[0] > size[0] - self.distance - self.block_width:
            self.position[0] = size[0] - self.distance - self.block_width
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
    def __init__(self,position,block_width,distance,number):
        super().__init__(position,block_width,number,'Vertical')
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
    score_font = pygame.font.Font(os.path.join(PATH,"Score_Font.ttf"), 40) 
    all_sprites_group = pygame.sprite.Group()
    player_group = pygame.sprite.Group()
    block_group = pygame.sprite.Group()
    block_count = 0
    player = Player()
    block_width = 90
    vertical_distance = 60
    block_y = size[1] - 20
    block_x = random.randint(80,size[0] - 80)
    start_block = Block([0,block_y],size[0],block_count)
    block_count += 1
    all_sprites_group.add(start_block)
    while block_y > 70:
        block_y -= random.randint(50,100)
        block_x = (block_x + (random.randint(-330,330))) % (size[0] - block_width)
        new_block = Block([block_x,block_y], block_width,block_count)
        block_count += 1
        block_group.add(new_block)
        all_sprites_group.add(new_block)
    player_group.add(player)
    all_sprites_group.add(player)
    game_over = False
    clock = pygame.time.Clock()
    current_block = 0
    current_pos = [size[0]//2,size[1] - 20]
    current_centre = [0,0]
    current_type = 'Still'
    horizontal_direction = 'none'
   
    
# -------------- Main Program Loop ---------------- #
    while not game_over:
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
                pygame.quit()
                return 'gameover'
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    game_over = True
        
        player.height = start_block.rect.top - player.rect.bottom 

        if player.height > player.score:
            player.score = player.height

        for block in block_group:
            if block.number == current_block + 1:
                next_pos = block.rect.topleft
                next_type = block.Type
                if block.Type == 'Still':
                    next_centre = block.rect.center
                else: 
                    next_centre = block.position
                next_direction = block.direction 
        
        horizontal_direction = Test_API.move(player.rect.center,current_pos,next_pos,next_type,next_centre,player.normal_speed,player.speed,size,player.direction,next_direction,block_width,horizontal_direction,current_type,current_centre)
        if horizontal_direction == 'right':
            player.rect.x += 9
        elif horizontal_direction == 'left':
            player.rect.x -= 9
        
        block_hit_list = pygame.sprite.spritecollide(player,block_group,False)
        for block in block_hit_list:
            
            if player.rect.bottom > block.rect.top and player.direction == 'down':
                current_block = block.number
                current_pos = block.rect.center
                current_type = block.Type
                current_centre = block.position
                player.reverse()
        if player.rect.colliderect(start_block):
            if player.rect.bottom > start_block.rect.top and player.direction == 'down':
                player.reverse()
        if player.rect.y < size[0]//4 :            
            if block_y > 0:
                temp_y = random.randint(50,100)
                block_y -= temp_y
                block_x = (block_x + (random.randint(-340,340))) % (size[0] - block_width)
                if block_y < 300:
                    block_type = random.choice(['move','still','still','still','still','vertical'])
                else:
                    block_type = 'still'
                if block_type == 'move':
                    new_block = SideBlock([block_x,block_y], block_width,block_count)
                elif block_type == 'still':
                    new_block = Block([block_x,block_y], block_width,block_count)
                elif block_type == 'vertical':
                    block_y -= (vertical_distance + temp_y)
                    new_block = VerticalBlock([block_x,block_y], block_width, vertical_distance,block_count)
                    block_y -= vertical_distance
                block_count += 1
                block_group.add(new_block)
                all_sprites_group.add(new_block)
            block_y = move(4,block_y,all_sprites_group)
            
        for block in block_group:
            if block.rect.y > size[1] + 50:
                block.kill()
        
        if player.rect.bottom > size[1]:
            game_over = True
            return 'gameover'
            #player.reverse()

            
        screen.blit(background_image_1,(0,0))
        all_sprites_group.update()
        player_group.draw(screen)
        block_group.draw(screen)

        score_display = score_font.render(str(player.score), True, BLACK)
        screen.blit(score_display,(size[0]//20, size[1]//20))

        pygame.display.flip()

        clock.tick(60)

def gameover():
    gameover_font = pygame.font.Font('freesansbold.ttf', 80) 
    screen.fill(BLACK) 
    Play = gameover_font.render('GAME OVER', True, WHITE)
    PlayRect = Play.get_rect()
    PlayRect.center = (size[0]//2, size[1]//2)
    screen.blit(Play, PlayRect) 
    pygame.display.flip()
    for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
    time.sleep(1)


if __name__ == '__main__':
    pygame.init()
    size = (1280,720)
    screen = pygame.display.set_mode(size)
    background_image_1 = pygame.image.load(os.path.join(PATH,"images","Background.jpg")).convert()
    background_image_1 = pygame.transform.smoothscale(background_image_1, size)
    while True:
        if gameplay() == 'gameover':
            gameover()

