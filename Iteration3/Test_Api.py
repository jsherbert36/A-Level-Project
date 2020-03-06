def GO(player_pos,current_pos,next_pos,next_type,next_centre,normal_speed,player_speed,size,player_direction,next_direction,block_width,horizontal_direction):
    if abs(next_pos[0] - player_pos[0]) > size[0]//2:
        if player_pos[0] < next_pos[0]:
            return 'left'
        elif player_pos[0] > next_pos[0]:
            return 'right'
        else: return 'none'
    elif player_pos[0] < next_pos[0]:
        return 'right'
    elif player_pos[0] > next_pos[0] + block_width:
        return 'left'
    else:
        return 'none'
    
def move(player_pos,current_pos,next_pos,next_type,next_centre,normal_speed,player_speed,size,player_direction,next_direction,block_width,horizontal_direction):
    direction = GO(player_pos,current_pos,next_pos,next_type,next_centre,normal_speed,player_speed,size,player_direction,next_direction,block_width,horizontal_direction)
    if next_type == 'Still':
        return direction
    elif next_type == 'Vertical':
        if (next_pos[1] > next_centre + 40 and next_direction == 'down') or horizontal_direction != 'none':
            return direction
        else:
            return 'none'
    elif next_type == 'Horizontal':
        if direction == 'left' and (next_pos[0] < next_centre - 80 or horizontal_direction == 'left'):
            return direction
        elif direction == 'right' and (next_pos[0] > next_centre + 80 or horizontal_direction == 'right'):
            return direction
        else:
            if player_pos[0] > current_pos[0] + (block_width//2):
                return 'left'
            elif player_pos[0] < current_pos[0] + (block_width//2):
                return 'right'
            else:
                return 'none'
    
