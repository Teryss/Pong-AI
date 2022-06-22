import pygame
import random

def Get_starting_info(all):
    players_info = {
        'p1_pos' : [10,150],
        'p2_pos' : [380,150],
        'MS' : 0.5,
    }
    ball_info = {
        'radius' : 5,
        'pos' : [200,180],
        'speed' : 0.4,
        'direction' : [0.7 if random.randint(0,1) == 0 else -0.7, random.randint(-6,6) * 0.1],
    }
    game_info = {
        'fps' : 120,
        'delta_time' : 0,
        'font' : pygame.font.Font(None, 30),
        'score' : [0,0],
        'ai_score' : [0,0]
    }
    if all:
        return players_info, ball_info, game_info
    else:
        return players_info, ball_info

def Restart(added_score, game_info):
    player_info, ball_info = Get_starting_info(all = False)

    if added_score == 'p_1':
        game_info['score'][0] += 1
    else:
        game_info['score'][1] += 1
    return player_info, ball_info, game_info

def AI_training_reset():
    p1_pos = [10,150]
    p2_pos = [380,150]
    ball_pos = [200,180]
    ball_dir = [1,0]
    return p1_pos, p2_pos, ball_pos, ball_dir
    

def drawBoardAndPlayers(window, colour, player_info, ball_info):
    window.fill( (0,0,0) )
    pygame.draw.rect(window, colour, (player_info['p2_pos'][0], player_info['p2_pos'][1],10,50))
    pygame.draw.rect(window, colour, (player_info['p1_pos'][0], player_info['p1_pos'][1],10,50))
    pygame.draw.circle(window, colour, ball_info['pos'], ball_info['radius'])

def drawScore(window, colour, font, score):
    score1_obj = font.render(str(score[0]), 1, colour)
    score2_boj = font.render(str(score[1]), 1, colour)
    window.blit(score1_obj, (150, 30))
    window.blit(score2_boj, (250, 30))


def player_movement(keys, player_info, dt, only_left):
    if keys[pygame.K_w] and player_info['p1_pos'][1] > 0:
        player_info['p1_pos'][1] -= player_info['MS'] * dt
    if keys[pygame.K_s] and player_info['p1_pos'][1] < 350:
        player_info['p1_pos'][1] += player_info['MS'] * dt
    if only_left == False:
        if keys[pygame.K_UP] and player_info['p2_pos'][1] > 0:
           player_info['p2_pos'][1] -= player_info['MS'] * dt
        if keys[pygame.K_DOWN] and player_info['p2_pos'][1] < 350:
            player_info['p2_pos'][1] += player_info['MS'] * dt

    return player_info

def AI_movement(decision, player, player_MS, dt):
    if decision == 0:
        return player
    elif decision == 1:
        if player[1] < 350:
            player[1] += player_MS * dt
    else:
        if player[1] > 0:
            player[1] -= player_MS * dt 
    return player

def ball_movement(ball_info, player_info, game_info):
    if ball_info['pos'][0] <= player_info['p1_pos'][0] +10 or ball_info['pos'][0] >= player_info['p2_pos'][0]:
        if ( player_info['p1_pos'][1] <= ball_info['pos'][1] <= player_info['p1_pos'][1] + 50 and ball_info['direction'][0] < 0 ) or ( player_info['p2_pos'][1] <= ball_info['pos'][1] <= player_info['p2_pos'][1] + 50 and ball_info['direction'][0] > 0 ):
            if ball_info['direction'][0] > 0:
                distance = player_info['p2_pos'][1] + 25 - ball_info['pos'][1]
                game_info['ai_score'][1] += 1
            else:
                distance = player_info['p1_pos'][1] + 25 - ball_info['pos'][1]
                game_info['ai_score'][0] += 1
            if distance > 25:
                distance = 24
            if distance < -25:
                distance = -24

            ball_info['direction'][1] = (1 - distance) / 25
            ball_info['direction'][0] *= -1
    if ball_info['pos'][1] >= 400 - ball_info['radius'] or ball_info['pos'][1] <= 0 + ball_info['radius']:
        ball_info['direction'][1] *= -1

    if ball_info['pos'][0] <= 0 or ball_info['pos'][0] >= 400:
        return 'p_2' if ball_info['pos'][0] < 0 else 'p_1'

    ball_info['pos'][0] += ball_info['speed'] * game_info['delta_time'] * ball_info['direction'][0]
    ball_info['pos'][1] += ball_info['speed'] * game_info['delta_time'] * ball_info['direction'][1]
    return ''