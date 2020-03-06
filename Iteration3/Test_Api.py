import tensorflow, numpy, math
def move(player_pos,current_pos,next_pos,next_type,next_centre,normal_speed,player_speed):
    if player_speed >= normal_speed:
        if next_pos[0] > current_pos:
            return right
    
