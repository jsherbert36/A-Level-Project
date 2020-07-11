import math,pygame,random,sys,os,neat,pickle,shelve,json
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
PATH = sys.path[0]
generation = 0
high_score = 0
high_net = None
slow = False
max_score_list = []
game_over = False

class Computer(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.width = 40
        self.image_list = []
        for i in range(1,9):
            temp_image = pygame.image.load(os.path.join(PATH,"images",("frame-"+str(i)+ ".png"))).convert_alpha()
            self.image_list.append(pygame.transform.smoothscale(temp_image, [self.width, self.width]))
        self.image = self.image_list[0]
        self.image_num = 0
        self.rect = self.image.get_rect()
        self.rect.x = SIZE[0]//2
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
        self.final_distance2 = []
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
                self.fitness += 5

    def set_score(self,start_block):
        self.height = start_block.rect.top - self.rect.bottom 
        if self.height > self.score:
            self.score = self.height
            self.score_count = 0
        if self.block_count > 2:
            self.fitness -= 1
            self.block_count = 0
        if self.none_score > 250:
            self.fitness -= 2
            self.none_score = 0

    def move(self):
        if self.horizontal_direction == 'right':
            self.rect.x += 9
        elif self.horizontal_direction == 'left':
            self.rect.x -= 9

    def check_directions(self,SIZE,block_group):        
        self.final_distance = [-1,-1,-1,-1] #[right,left,down,up]
        right_rect = pygame.Rect(self.rect.right, self.rect.y, SIZE[0], self.width)
        distance = []
        for block in block_group:
            if right_rect.colliderect(block.rect): distance.append(block.rect.x - right_rect.right)
        if len(distance) > 0: self.final_distance[0] = min(distance)
        distance = []
        left_rect = pygame.Rect(0 ,self.rect.y, self.rect.left, self.width)
        for block in block_group:
            if left_rect.colliderect(block.rect): distance.append(self.rect.right - block.rect.left)
        if len(distance) > 0: self.final_distance[1] = min(distance)
        distance = []
        down_rect = pygame.Rect(self.rect.x, self.rect.bottom, self.width, SIZE[0] - self.rect.bottom)
        for block in block_group:
            if down_rect.colliderect(block.rect): distance.append(block.rect.top - self.rect.bottom)
        if len(distance) > 0: self.final_distance[2] = min(distance)
        distance = []
        up_rect = pygame.Rect(self.rect.x, 0, self.width, self.rect.top)
        for block in block_group:
            if up_rect.colliderect(block.rect): distance.append(self.rect.top - block.rect.bottom)
        if len(distance) > 0: self.final_distance[3] = min(distance)
        return self.final_distance

    def check_quadrants(self,SIZE,block_group):
        self.final_distance2 = [-1,-1,-1,-1]
        distance = [[],[],[],[]]
        for block in block_group:
            if block.rect.centerx > self.rect.centerx and block.rect.centery < self.rect.centery:
                distance[0].append(math.hypot((block.rect.centerx - self.rect.centerx),(self.rect.centery - block.rect.centery)))
            elif block.rect.centerx < self.rect.centerx and block.rect.centery > self.rect.centery:
                distance[1].append(math.hypot((self.rect.centerx - block.rect.centerx),(block.rect.centery - self.rect.centery)))
            elif block.rect.centerx < self.rect.centerx and block.rect.centery < self.rect.centery:
                distance[2].append(math.hypot((self.rect.centerx - block.rect.centerx),(self.rect.centery - block.rect.centery)))
            elif block.rect.centerx > self.rect.centerx and block.rect.centery > self.rect.centery:
                distance[3].append(math.hypot((block.rect.centerx - self.rect.centerx),(block.rect.centery - self.rect.centery)))
        for i in range(4):
            if len(distance[i]) > 0:
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
        self.rect.x, self.rect.y = position

    def update(self):
        pass

class SideBlock(Block):
    def __init__(self,position,block_width,number):
        super().__init__(position,block_width,number)
        self.direction = random.choice(['left','right'])
        self.distance = 120
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
    def __init__(self,position,block_width,distance,number):
        super().__init__(position,block_width,number)
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

def move(direction,block_y,block_group,player_list,start_block):
    for block in block_group:
        block.rect.y += direction
        if isinstance(block,VerticalBlock):
            block.position[1] += direction 
    for player in player_list:
        player.rect.y += direction
    start_block.rect.y += direction
    block_y += direction
    return block_y
    
def set_block(block_x,block_y,block_width,tolerance):
    block_y -= random.randint(130,140)
    far_left = block_x - block_width//2
    far_right = SIZE[0]- block_x - block_width
    block_x += random.randint(-1 * min(tolerance,far_left),min(far_right,tolerance))
    return block_x,block_y

def choose_block_type(height):
    if height > 3000 and height < 10000:
        return random.choice(['move','still','still','still','still','still','vertical'])
    elif height >= 10000:
        return random.choice(['move','still','still','still','vertical'])
    else:
        return 'still'
    
def gameplay(genomes,config):
    global game_over
    if game_over:
        for genome_id,genome in genomes: 
            genome.fitness = 0
        return
    global generation,high_net,high_score,slow
    background_image_1 = pygame.image.load(os.path.join(PATH,"images","Background.jpg")).convert()
    background_image_1 = pygame.transform.smoothscale(background_image_1, SIZE)
    generation += 1
    score_font = pygame.font.Font("freesansbold.ttf", 30) 
    player_list = []
    genome_list = []
    nn_list = []
    block_group = pygame.sprite.Group()
    block_count = 0
    tolerance = 220
    vertical_distance = 60

    for genome_id,genome in genomes:
        genome.fitness = 0
        net = neat.nn.FeedForwardNetwork.create(genome, config)
        nn_list.append(net)
        player_list.append(Computer())
        genome_list.append(genome)

    block_width = 130
    start_block = Block([0,SIZE[1]-20],SIZE[0],block_count)
    block_count += 1
    block_x,block_y = SIZE[0]//2,SIZE[1] - 50
    new_block = Block([block_x,block_y], block_width,block_count)
    block_count += 1
    block_group.add(new_block)
    while block_y > 70:
        block_x,block_y = set_block(block_x,block_y,block_width,tolerance) 
        new_block = Block([block_x,block_y], block_width,block_count)
        block_count += 1
        block_group.add(new_block)  
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
                return
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    game_over = True
                    return 
                elif event.key == pygame.K_SPACE:
                    slow = not slow

        screen.blit(background_image_1,(0,0)) 
        current_score = 0
        for i,player in enumerate(player_list):
            player.score_count += 1
            player.set_score(start_block)
            genome_list[i].fitness = player.fitness 
            player.move()
            player.collision(block_group)
            if player.score > current_score:
                current_score = player.score
                max_index = i
                max_net = nn_list[i]
            if player.score > max_score:
                max_score = player.score
            distance1 = player.check_directions(SIZE,block_group)
            distance2 = player.check_quadrants(SIZE,block_group)
            nn_output = nn_list[i].activate(distance1 + distance2)
            position = nn_output.index(max(nn_output))
            if position == 0 and nn_output[0] > 0.5:
                player.horizontal_direction = 'right'
                player.none_score = 0
            elif position == 1 and nn_output[1] > 0.5:
                player.horizontal_direction = 'left'
                player.none_score = 0
            elif player.horizontal_direction != 'none':
                player.none_score = 0
                player.horizontal_direction = 'none'
            else:
                player.none_score += 1
        
        if max_index >= len(player_list):
            max_index = len(player_list) - 1
        print(player_list[max_index].fitness,player_list[max_index].final_distance,player_list[max_index].final_distance2)
        if player_list[max_index].rect.y < SIZE[0]//5 :            
            if block_y > -10:
                block_x,block_y = set_block(block_x,block_y,block_width,tolerance)                
                block_type = choose_block_type(player_list[max_index].score)
                if block_type == 'move':
                    new_block = SideBlock([block_x,block_y], block_width,block_count)
                elif block_type == 'still':
                    new_block = Block([block_x,block_y], block_width,block_count)
                elif block_type == 'vertical':
                    block_y -= vertical_distance//2 
                    new_block = VerticalBlock([block_x,block_y], block_width, vertical_distance,block_count)
                    block_y -= vertical_distance//2            
                block_count += 1
                block_group.add(new_block)

        if count % 15 == 0:
            block_width = int(round(-60/(1+1.0001**(9000-max_score)) + 160))

        if count % 13 == 0:
            tolerance = int(round(60/(1+1.0003**(10000-max_score)) + 190))

        if player_list[max_index].rect.y < 0:
            block_y = move(11,block_y,block_group,player_list,start_block)
        elif player_list[max_index].rect.y < SIZE[1]//6 and player_list[max_index].rect.y > 0:
            block_y = move(7,block_y,block_group,player_list,start_block)
        elif player_list[max_index].rect.y < SIZE[1]//3 and player_list[max_index].rect.y > SIZE[1]//6:
            block_y = move(4,block_y,block_group,player_list,start_block)
            
        for block in block_group:
            if block.rect.y > SIZE[1] * 2:
                block.kill()

        for player in player_list:
            if player.rect.bottom > SIZE[1]* 2 or player.score_count > 450:
                genome_list[player_list.index(player)].fitness = player.fitness
                nn_list.pop(player_list.index(player))
                genome_list.pop(player_list.index(player))
                player_list.pop(player_list.index(player))

        screen.blit(background_image_1,(0,0))     
        block_group.update()
        block_group.draw(screen)
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
        high_net = max_net
    max_score_list.append(max_score)

def run(window,surface):
    global SIZE,screen,game_over
    config_file = os.path.join(PATH,"config2.txt")
    SIZE = window
    screen = surface
    config = neat.config.Config(neat.DefaultGenome, neat.DefaultReproduction, neat.DefaultSpeciesSet, neat.DefaultStagnation,config_file)
    population = neat.Population(config)
    best_genome = population.run(gameplay, 200)
    if __name__ == "__main__" and not game_over:
        test_database = shelve.open("test_database")
        test_database["test"] = high_net
        test_database.close()
        f = open("score_list.json","wt")        
        json.dump(max_score_list, f)
        f.close()


if __name__ == '__main__':
    os.environ['SDL_VIDEO_CENTERED'] = '1'
    pygame.init()
    SIZE = (1280,720)
    screen = pygame.display.set_mode(SIZE)
    pygame.display.set_caption("NEAT-JUMP")
    run(SIZE,screen)

