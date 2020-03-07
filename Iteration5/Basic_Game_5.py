import math,pygame,random,sys,os,time,neat,numpy,pickle
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
        self.rect.x = numpy.random.randint(0,SIZE[0])
        self.rect.y = SIZE[1] - self.width
        self.direction = 'up'
        self.normal_speed = 20
        self.speed = self.normal_speed
        self.terminal_velocity = 22
        self.height = 0
        self.score = 0
        self.current_block = 0
        self.current_pos = [SIZE[0]//2,SIZE[1] - 20]
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
        if self.rect.x > SIZE[0] - self.width + 10:
            self.rect.x = 1
        elif self.rect.x < 0:
            self.rect.x = SIZE[0] - self.width
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
    
def sigmoid(X):
   return 1/(1+np.exp(-X))
    
def gameplay(genomes,config):
    global generation
    generation += 1
    POPULATION_SIZE = 40
    score_font = pygame.font.Font("freesansbold.ttf", 35) 
    player_list = []
    genome_list = []
    nn_list = []
    block_list = []
    block_count = 0

    for genome_id,genome in genomes:
        genome.fitness = 0
        net = neat.nn.FeedForwardNetwork.create(genome, config)
        nn_list.append(net)
        player_list.append(Player())
        genome_list.append(genome)


    block_width = 90
    block_y = SIZE[1] - 20
    block_x = random.randint(80,SIZE[0] - 80)
    start_block = Block([0,block_y],SIZE[0],block_count)
    block_count += 1
    while block_y > 70:
        block_y -= random.randint(50,100)
        block_x = (block_x + (random.randint(-325,325))) % (SIZE[0] - block_width)
        new_block = Block([block_x,block_y], block_width,block_count)
        block_count += 1
        block_list.append(new_block)   
    game_over = False
    clock = pygame.time.Clock()
    horizontal_direction = 'none'
    current_score = 0
    max_index = 0
    max_score = 0
    score_count = 0
# -------------- Main Program Loop ---------------- #
    while not game_over and len(player_list) > 0:

        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
                pygame.quit()
                quit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    game_over = True
                    return 'gameover'
        current_score = 0
        score_count += 1
        if score_count > 700:
            game_over = True

        for i,player in enumerate(player_list):
            if player.alive == True:
                player.set_score(start_block)
                genome.fitness += player.score/100000
                player.set_next(block_list) 
                player.move()
                player.collision(block_list,start_block)
                if player.score > current_score:
                    current_score = player.score
                    max_index = i
                if player.score > max_score:
                    max_score = player.score
                    score_count = 0
                nn_output = nn_list[i].activate((player.rect.centerx,player.rect.centery,player.current_pos[0],player.current_pos[1],player.next_pos[0],player.next_pos[1]))
                map(sigmoid,nn_output)
                position = nn_output.index(max(nn_output))
                if position == 0:
                    player.horizontal_direction = 'right'
                elif position == 1:
                    player.horizontal_direction = 'none'
                elif position == 2:
                    player.horizontal_direction = 'left'

        if max_index >= len(player_list):
            max_index = len(player_list) - 1
        

        if player_list[max_index].rect.y < SIZE[0]//4 :            
            if block_y > 0:
                temp_y = random.randint(50,100)
                block_y -= temp_y
                block_x = (block_x + (random.randint(-340,340))) % (SIZE[0] - block_width)
                new_block = Block([block_x,block_y], block_width,block_count)
                block_count += 1
                block_list.append(new_block)
            block_y = move(4,block_y,block_list,player_list,start_block)
            
        for block in block_list:
            if block.rect.y > SIZE[1] + 30:
                block.alive = False
                block_list.pop(block_list.index(block))

        for player in player_list:
            if player.rect.bottom > SIZE[1]:
                player.alive = False
                
                genome_list[player_list.index(player)].fitness -= 3
                nn_list.pop(player_list.index(player))
                genome_list.pop(player_list.index(player))
                player_list.pop(player_list.index(player))

        if max_score > 120000:
            f = open("best.pickle","wb")
            pickle.dump(nn_list[0],f)
            f.close()
            game_over = True
        
        #if all(player.alive == False for player in player_list):
        #    game_over = True
        #    return 'gameover'

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
        screen.blit(score_display,(SIZE[0]//20, SIZE[1]//20))

        pygame.display.flip()
        clock.tick(60)

def run(config_file):
    config = neat.config.Config(neat.DefaultGenome, neat.DefaultReproduction, neat.DefaultSpeciesSet, neat.DefaultStagnation,config_file)
    population = neat.Population(config)
    population.add_reporter(neat.StdOutReporter(True))
    statistics = neat.StatisticsReporter()
    population.add_reporter(statistics)
    winner = population.run(gameplay, 50)
    print('\nBest genome:\n{!s}'.format(winner))


if __name__ == '__main__':
    pygame.init()
    SIZE = (1280,720)
    screen = pygame.display.set_mode(SIZE)
    pygame.display.set_caption("NEAT-Jump")
    background_image_1 = pygame.image.load(os.path.join(PATH,"images","Background.jpg")).convert()
    background_image_1 = pygame.transform.smoothscale(background_image_1, SIZE)
    generation = 0
    run(os.path.join(PATH,"config-feedforward.txt"))

