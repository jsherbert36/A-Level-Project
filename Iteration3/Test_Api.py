def move(player_pos,current_pos,next_pos,next_type,next_centre,normal_speed,player_speed,size,player_direction,next_direction,block_width,horizontal_direction,current_type,current_centre):
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
    if current_type == 'Still': Go = True
    elif current_type == 'Vertical':
        if current_pos[1] > current_centre[1] + 40  or horizontal_direction != 'none':
            Go = True
        else:
            Go = False
    elif current_type == 'Horizontal':
        if direction == 'left' and (current_pos[0] < current_centre[0] - 80 or horizontal_direction == 'left'):
            Go = True
        elif direction == 'right' and (current_pos[0] > current_centre[0] + 80 or horizontal_direction == 'right'):
            Go = True
        else:
            Go = False
    if horizontal_direction == 'none':
        if current_pos[1] - player_pos[1] > 40 and player_direction == 'up':
            Go = True
        else: 
            Go = False
    print(Go)
    if Go == True:
        if next_type == 'Still':
            return direction
        elif next_type == 'Vertical':
            if (next_pos[1] > next_centre[1] + 40 and next_direction == 'down') or horizontal_direction != 'none':
                return direction
            elif current_type == 'Vertical':
                return direction
            else:
                return 'none'
        elif next_type == 'Horizontal':
            if direction == 'left' and (next_pos[0] > next_centre[0] + 60 or horizontal_direction == 'left'):
                return direction
            elif direction == 'right' and (next_pos[0] < next_centre[0] - 60 or horizontal_direction == 'right'):
                return direction
    elif current_type == 'Horizontal':
        if player_pos[0] > current_pos[0] + (block_width//2):
            return 'left'
        elif player_pos[0] < current_pos[0] + (block_width//2):
            return 'right'
        else:
            return 'none'
    else:
        return 'none'
