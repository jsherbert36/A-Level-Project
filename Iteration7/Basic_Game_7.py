import math,pygame,random,sys,os,time,neat,pickle
import numpy as np
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
        self.rect.x = 25
        self.rect.y = SIZE[1] - self.width
        self.direction = 'up'
        self.normal_speed = 22
        self.speed = self.normal_speed
        self.terminal_velocity = 24
        self.height = 0
        self.score = 0
        self.current_block = 0
        self.current_pos = [SIZE[0]//2,SIZE[1] - 20]
        self.horizontal_direction = 'none'
        self.score_count = 0
        self.final_distance = []
        self.block_hit_list = []
        self.fitness = 0
        self.block_count = 0
        self.none_score = 0

    def update(self):
        self.image_num = (self.image_num + 1 ) % 14
        if self.image_num % 3 == 0:
            self.image = self.image_list[self.image_num//2]
        if self.direction == 'up':
            self.rect.y -= self.speed
        elif self.direction == 'down':
            self.rect.y += self.speed
        self.change_speed()
        if self.rect.right > SIZE[0]:
            self.rect.right = 0
        elif self.rect.x < 0:
            self.rect.x = SIZE[0]
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

    def collision(self,block_group):
        block_hit_list = pygame.sprite.spritecollide(self,block_group,False)
        for block in block_hit_list:
            if self.rect.bottom > block.rect.top and self.direction == 'down':
                if self.current_block == block.number:
                    self.block_count += 1
                else:
                    self.current_block = block.number
                    self.block_count = 0
                self.current_pos = block.rect.midtop
                self.reverse()
            if block.number not in self.block_hit_list:
                self.block_hit_list.append(block.number)
                self.fitness += 3

    def set_score(self,start_block):
        self.height = start_block.rect.top - self.rect.bottom 
        if self.height > self.score:
            self.score = self.height
            self.score_count = 0
        if self.block_count > 2:
            self.fitness -= 1
            self.block_count = 0
        if self.none_score > 500:
            self.fitness -= 2
            self.none_score = 0

    def move(self):
        if self.horizontal_direction == 'right':
            self.rect.x += 9
        elif self.horizontal_direction == 'left':
            self.rect.x -= 9

    def check_directions(self,SIZE,block_list):
        temp_rect = self.rect
        self.final_distance = [0,0,0,0] #[right,left,down,up]
        self.rect = pygame.Rect(self.rect.x, self.rect.y, SIZE[0], self.width)
        distance = [math.inf]
        for block in block_list:
            if self.rect.colliderect(block.rect):
                distance.append(abs(block.rect.x + block.block_width - self.rect.x + self.width/2))
        if len(distance) > 1:
            self.final_distance[0] = min(distance)
        distance = [math.inf]
        self.rect = temp_rect
        self.rect = pygame.Rect(self.rect.x - SIZE[0], self.rect.y, SIZE[0], self.width)
        for block in block_list:
            if self.rect.colliderect(block.rect):
                distance.append(abs(block.rect.x + block.block_width - self.rect.x + self.width/2))
        if len(distance) > 1:
            self.final_distance[1] = min(distance)
        distance = [math.inf]
        self.rect = temp_rect
        self.rect = pygame.Rect(self.rect.x, self.rect.y, self.width, SIZE[0])
        for block in block_list:
            if self.rect.colliderect(block.rect):
                distance.append(abs(block.rect.y + block.rect.height - self.rect.y - self.width/2))
        if len(distance) > 1:
            self.final_distance[2] = min(distance)
        distance = [math.inf]
        self.rect = temp_rect
        self.rect = pygame.Rect(self.rect.x, self.rect.y - SIZE[0], self.width, SIZE[0])
        for block in block_list:
            if self.rect.colliderect(block.rect):
                distance.append(abs(block.rect.y + block.rect.height - self.rect.y - self.width/2))
        if len(distance) > 1:
            self.final_distance[3] = min(distance)
        self.rect = temp_rect
        return self.final_distance

    def check_quadrants(self,SIZE,block_list):
        self.final_distance2 = [0,0,0,0]
        distance = [[math.inf],[math.inf],[math.inf],[math.inf]]
        for block in block_list:
            if block.rect.centerx > self.rect.centerx and block.rect.y < self.rect.y:
                distance[0].append(math.sqrt(((block.rect.centerx - self.rect.centerx)**2)+((self.rect.y - block.rect.y)**2)))
            elif block.rect.centerx < self.rect.centerx and block.rect.y > self.rect.y:
                distance[1].append(math.sqrt(((self.rect.centerx - block.rect.centerx)**2)+((block.rect.y - self.rect.y)**2)))
            elif block.rect.centerx < self.rect.centerx and block.rect.y < self.rect.y:
                distance[2].append(math.sqrt(((self.rect.centerx - block.rect.centerx)**2)+((self.rect.y - block.rect.y)**2)))
            elif block.rect.centerx > self.rect.centerx and block.rect.y > self.rect.y:
                distance[3].append(math.sqrt(((block.rect.centerx - self.rect.centerx)**2)+((block.rect.y - self.rect.y)**2)))
        for i in range(4):
            if len(distance[i]) > 1:
                self.final_distance2[i] = min(distance[i])
        return self.final_distance2
    
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

def move(direction,block_y,block_list,player_list,start_block):
    for block in block_list:
        block.rect.y += direction
    for player in player_list:
        player.rect.y += direction
    start_block.rect.y += direction
    block_y += direction
    return block_y
    
def set_block(block_x,block_y,block_width,tolerance):
    block_y -= random.randint(130,140)
    block_x = (block_x + np.random.randint(-1 * tolerance,tolerance)) % SIZE[0]
    if block_x > SIZE[0] - block_width:
        block_x -= block_width
    return block_x,block_y
    
def gameplay(genomes,config):
    global generation
    global high_score
    global slow
    generation += 1
    score_font = pygame.font.Font("freesansbold.ttf", 30) 
    player_list = []
    genome_list = []
    nn_list = []
    block_list = []
    block_count = 0
    tolerance = 220

    for genome_id,genome in genomes:
        genome.fitness = 0
        net = neat.nn.FeedForwardNetwork.create(genome, config)
        nn_list.append(net)
        player_list.append(Player())
        genome_list.append(genome)

    block_width = 130
    start_block = Block([0,SIZE[1]-20],SIZE[0],block_count)
    block_count += 1
    block_x,block_y = 25,SIZE[1] - 50
    new_block = Block([block_x,block_y], block_width,block_count)
    block_count += 1
    block_list.append(new_block)
    while block_y > 70:
        block_x,block_y = set_block(block_x,block_y,block_width,tolerance) 
        new_block = Block([block_x,block_y], block_width,block_count)
        block_count += 1
        block_list.append(new_block)   
    game_over = False
    clock = pygame.time.Clock()
    current_score = 0
    max_index = 0
    max_score = 0
    count = 0

# -------------- Main Program Loop ---------------- #
    while not game_over and len(player_list) > 0:
        count += 1
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
                pygame.quit()
                quit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    game_over = True
                elif event.key == pygame.K_q:
                    slow = not slow
        
        current_score = 0
        for i,player in enumerate(player_list):
            player.score_count += 1
            player.set_score(start_block)
            genome_list[i].fitness = player.fitness 
            player.move()
            player.collision(block_list)
            if player.score > current_score:
                current_score = player.score
                max_index = i
            if player.score > max_score:
                max_score = player.score
            distance1 = player.check_directions(SIZE,block_list)
            distance2 = player.check_quadrants(SIZE,block_list)
            nn_output = nn_list[i].activate(distance1 + distance2)
            position = nn_output.index(max(nn_output))
            if position == 0 and nn_output[0] > 0.5:
                player.horizontal_direction = 'right'
                player.none_score = 0
            elif position == 1 and nn_output[1] > 0.5:
                player.horizontal_direction = 'left'
                player.none_score = 0
            else:
                if player.horizontal_direction != 'none':
                    player.none_score = 0
                    player.horizontal_direction = 'none'
                else:
                    player.none_score += 1
        
        if max_index >= len(player_list):
            max_index = len(player_list) - 1

        if player_list[max_index].rect.y < SIZE[1]//4 :            
            if block_y > -10:
                block_x,block_y = set_block(block_x,block_y,block_width,tolerance)
                new_block = Block([block_x,block_y], block_width,block_count)
                block_count += 1
                block_list.append(new_block)

        if count % 15 == 0:
            block_width = int(round(-60/(1+1.0003**(5000-max_score)) + 160))

        if count % 13 == 0:
            tolerance = int(round(60/(1+1.0003**(5000-max_score)) + 190))

        if player_list[max_index].rect.y < 0:
            block_y = move(11,block_y,block_list,player_list,start_block)
        elif player_list[max_index].rect.y < SIZE[1]//6 and player_list[max_index].rect.y > 0:
            block_y = move(7,block_y,block_list,player_list,start_block)
        elif player_list[max_index].rect.y < SIZE[1]//3 and player_list[max_index].rect.y > SIZE[1]//6:
            block_y = move(4,block_y,block_list,player_list,start_block)
            
        for block in block_list:
            if block.rect.y > SIZE[1] + 30:
                block_list.pop(block_list.index(block))

        for player in player_list:
            if player.rect.top > SIZE[0] or player.score_count > 500:
                genome_list[player_list.index(player)].fitness = player.fitness
                nn_list.pop(player_list.index(player))
                genome_list.pop(player_list.index(player))
                player_list.pop(player_list.index(player))

        screen.blit(background_image_1,(0,0))     
        for block in block_list:
            block.update
            screen.blit(block.image,block.rect)
        for player in player_list:
            player.update()
            screen.blit(player.image,player.rect)

        score_display = score_font.render("Max Score " + str(max_score), True, BLACK)
        screen.blit(score_display,(SIZE[0]//20, SIZE[1]//20))
        generation_display = score_font.render("Generation " + str(generation), True, BLACK)
        screen.blit(generation_display,(SIZE[0]//20, SIZE[1]//10))
        high_score_display = score_font.render("Highscore " + str(high_score), True, BLACK)
        screen.blit(high_score_display,(SIZE[0]//20, SIZE[1]//7))

        pygame.display.flip()
        if slow == True:
            clock.tick(60)
    if max_score > high_score:
        high_score = max_score

def run(config_file):
    config = neat.config.Config(neat.DefaultGenome, neat.DefaultReproduction, neat.DefaultSpeciesSet, neat.DefaultStagnation,config_file)
    population = neat.Population(config)
    population.add_reporter(neat.StdOutReporter(True))
    statistics = neat.StatisticsReporter()
    population.add_reporter(statistics)
    winner = population.run(gameplay, 600)
    print('\nBest genome:\n{!s}'.format(winner))


if __name__ == '__main__':
    pygame.init()
    SIZE = (1280,720)
    screen = pygame.display.set_mode(SIZE)
    pygame.display.set_caption("NEAT-Jump")
    background_image_1 = pygame.image.load(os.path.join(PATH,"images","Background.jpg")).convert()
    background_image_1 = pygame.transform.smoothscale(background_image_1, SIZE)
    generation = 0
    high_score = 0
    slow = False
    run(os.path.join(PATH,"config2.txt"))

