

def move(player_pos,current_pos,next_pos,size,player_direction,block_width,horizontal_direction):
    if abs(next_pos[0] - player_pos[0]) > size[0]//2:
        if player_pos[0] < next_pos[0]:
            direction = 'left'
        elif player_pos[0] > next_pos[0]:
            direction = 'right'
        else: 
            direction = 'none'
    elif player_pos[0] < next_pos[0]:
        direction = 'right'
    elif player_pos[0] > next_pos[0] + block_width:
        direction = 'left'
    else:
        direction = 'none'
    
    if horizontal_direction == 'none':
        if current_pos[1] - player_pos[1] > 40 and player_direction == 'up':
            Go = True
        else: 
            Go = False
    else:
        Go = True
    if Go == True:
        return direction
    else:
        return 'none'
