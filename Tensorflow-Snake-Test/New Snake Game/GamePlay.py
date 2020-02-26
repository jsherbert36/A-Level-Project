import pygame,random
from queue import SimpleQueue
# Define some colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
BLUE = (0,0,255)
RED = (255, 0, 0)
class Apple(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.width = 10
        self.image = pygame.Surface([self.width,self.width])
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0,(size[0]-10)//self.width) * self.width
        self.rect.y = random.randint(0,(size[1]-10)//self.width) * self.width
    def reset(self):
        self.temp_x = random.randint(0,(size[0]-10)//self.width) * self.width
        self.temp_y = random.randint(0,(size[1]-10)//self.width) * self.width
        for block in snake1.snake_group:
            if block.rect.Rect.collidepoint(self.temp_x,self.temp_y):
                

        
class Snake(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.width = 10
        self.Pos_Queue = SimpleQueue()
        self.Head_Block = [size[0]//2,size[1]//2]
        self.Pos_Queue.put(Head_Block)
        self.snake_group = pygame.sprite.Group()
        self.newsnake = SnakeBlock(self.Head_Block)
        self.snake_group.add(self.newsnake)
        
    def update(self):
        if self.direction == 'right':
            self.Pos_Queue.put(self.Head_Block)
            self.Head_Block[0] += self.width
        elif self.direction == 'left':
            self.Pos_Queue.put(self.Head_Block)
            self.Head_Block[0] -= self.width
        elif self.direction == 'up':
            self.Pos_Queue.put(self.Head_Block)
            self.Head_Block[1] -= self.width
        elif self.direction == 'down':
            self.Pos_Queue.put(self.Head_Block)
            self.Head_Block[1] += self.width
        self.newsnake = SnakeBlock(self.Head_Block)
        self.snake_group.add(self.newsnake)
        self.temp_last_block = self.Pos_Queue.get()
        for block in snake_group:
            if block.rect.x == self.temp_last_block[0] and self.rect.y == self.temp_last_block[1]:
                block.kill()
    def draw(self,display_):
        self.snake_group.draw(display_)
    def move(self,val):
        if val in ['right','left','down','up']:
            self.direction = val
    
class SnakeBlock(pygame.sprite.Sprite):
    def __init__(self,pos):
        super().__init__()
        self.width = 10
        self.length
        self.image = pygame.Surface([self.width, self.width])
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.rect.x = pos[0]
        self.rect.y = pos[1]

def gameplay()
    snake_group = pygame.sprite.Group()
    snake1 = Snake()
    snake_group.add(snake1)
    game_over = False
    # -------- Main Program Loop ----------- #
    while not game_over:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    game_over = True
            
        keys = pygame.key.get_pressed()
        if keys[pygame.K_RIGHT]:
            player1.move('right')
        elif keys[pygame.K_LEFT]:
            player1.move('left')
        elif keys[pygame.K_DOWN]:
            player1.move('down')
        elif keys[pygame.K_UP]:
            player1.move('up')

        if pygame.sprite.spritecollide(apple1, snake_group, False):
            apple.reset()
        for block in snake1.snake_group:
            if pygame.sprite.spritecollide(block, snake_group, False):
                game_over = True
        for block in snake1.snake_group:
            if block
        screen.fill(BLACK)
        apple1.draw(screen)
        snake1.draw(screen)
        clock.tick(50)
        pygame.display.flip()



User_Choice = input('Generate new maze? (Y/N): ')
block_width = int(input('Enter Block Size (integer):'))
pygame.init()
width = 700
height = 700
size = (width,height)
screen = pygame.display.set_mode(size)
clock = pygame.time.Clock()
while True:
    gameplay()
pygame.quit()
