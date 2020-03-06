import tensorflow, numpy, math
def GO(player_pos,current_pos,next_pos,next_type,next_centre,normal_speed,player_speed,size,player_direction,next_direction):
    if abs(next_pos[0] - current_pos[0]) > size[0]//2:
        if current_pos[0] < next_pos[0]:
            return 'left'
        elif current_pos[0] > next_pos[1]:
            return 'right'
        else: return None
    elif current_pos[0] < next_pos[0]:
        return 'right'
    elif current_pos[0] > next_pos[0]:
        return 'left'
    else: return None
def move(player_pos,current_pos,next_pos,next_type,next_centre,normal_speed,player_speed,size,player_direction,next_direction):
    if next_type == 'Still':
        return GO(player_pos,current_pos,next_pos,next_type,next_centre,normal_speed,player_speed,size,player_direction,next_direction)
    elif next_type == 'Vertical':
        if next_pos[1] > next_centre[1] and next_direction == 'down':
            return GO(player_pos,current_pos,next_pos,next_type,next_centre,normal_speed,player_speed,size,player_direction,next_direction)
        else:
            return None
    elif next_type == 'Horizontal':
        direction = GO(player_pos,current_pos,next_pos,next_type,next_centre,normal_speed,player_speed,size,player_direction,next_direction)
        if direction == 'left' and next_pos[0] > next_centre[0]:
            return direction
        elif direction == 'right' and next_pos[0] < next_centre[0]:
            return direction
        else: return None
    
