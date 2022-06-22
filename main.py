import os
import neat
import pygame
import pong
import pickle

def play_against_another_player():
    pygame.init()
    width, height = 400,400
    screen = pygame.display.set_mode((width,height))
    pygame.display.set_caption("Pong!")
    white = (255,255,255)
    players_info, ball_info, game_info = pong.Get_starting_info(all = True)
    last_frame_tick = 0
    clock = pygame.time.Clock()
    running = True
    while running:
        t = pygame.time.get_ticks()
        game_info['delta_time'] = t - last_frame_tick
        players_info= pong.player_movement(pygame.key.get_pressed(),players_info, game_info['delta_time'], only_left = False)
        detect_restart = pong.ball_movement(ball_info, players_info, game_info)
        pong.drawBoardAndPlayers(screen, white, players_info, ball_info)
        if detect_restart != '':
            players_info, ball_info, game_info = pong.Restart(detect_restart, game_info)

        pong.drawScore(screen, white, game_info['font'], game_info['score'])
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()

        last_frame_tick = t
        clock.tick(game_info['fps'])
        pygame.display.update()


def train_ai(screen, genome1, genome2, conf):
    pygame.init()
    white = (255,255,255)
    players_info, ball_info, game_info = pong.Get_starting_info(all = True)
    net1 = neat.nn.FeedForwardNetwork.create(genome1,conf)
    net2 = neat.nn.FeedForwardNetwork.create(genome2,conf)
    clock = pygame.time.Clock()
    running = True
    game_info['delta_time'] = 34
    while running:
        detect_restart = pong.ball_movement(ball_info, players_info, game_info)
        pong.drawBoardAndPlayers(screen, white, players_info, ball_info)
        if detect_restart != '' or game_info['ai_score'][0] > 50 or game_info['ai_score'][0] > 50:
            calculate_fitness(genome1, genome2, game_info['ai_score'])
            running = False
            break

        output1 = net1.activate((players_info['p2_pos'][1], ball_info['pos'][1], abs(players_info['p2_pos'][0] - ball_info['pos'][0])))
        decision1 = output1.index(max(output1))
        output2 = net2.activate((players_info['p1_pos'][1], ball_info['pos'][1], abs(players_info['p1_pos'][0] - ball_info['pos'][0])))
        decision2 = output2.index(max(output2))
        players_info['p1_pos'] = pong.AI_movement(decision1, players_info['p1_pos'], players_info['MS'], game_info['delta_time'])
        players_info['p2_pos'] = pong.AI_movement(decision2, players_info['p2_pos'], players_info['MS'], game_info['delta_time'])
        
        pong.drawScore(screen, white, game_info['font'], game_info['ai_score'])
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()
        clock.tick(game_info['fps'])
        pygame.display.update()

def play_against_ai(config):
    pygame.init()
    width, height = 400,400
    screen = pygame.display.set_mode((width,height))
    pygame.display.set_caption("Pong_training_ai!")
    with open('best.pickle', 'rb') as f:
        winner = pickle.load(f)
    net = neat.nn.FeedForwardNetwork.create(winner, config)
    white = (255,255,255)
    players_info, ball_info, game_info = pong.Get_starting_info(all = True)
    last_frame_tick = 0
    clock = pygame.time.Clock()
    running = True
    while running:
        t = pygame.time.get_ticks()
        game_info['delta_time'] = t - last_frame_tick
        players_info= pong.player_movement(pygame.key.get_pressed(),players_info, game_info['delta_time'], only_left = True)
        detect_restart = pong.ball_movement(ball_info, players_info, game_info)
        pong.drawBoardAndPlayers(screen, white, players_info, ball_info)
        if detect_restart != '':
            players_info, ball_info, game_info = pong.Restart(detect_restart, game_info)

        output= net.activate((players_info['p2_pos'][1], ball_info['pos'][1], abs(players_info['p2_pos'][0] - ball_info['pos'][0])))
        decision = output.index(max(output))
        players_info['p2_pos'] = pong.AI_movement(decision, players_info['p2_pos'], players_info['MS'], game_info['delta_time'])

        pong.drawScore(screen, white, game_info['font'], game_info['score'])
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()

        last_frame_tick = t
        clock.tick(game_info['fps'])
        pygame.display.update()

def calculate_fitness(genome1,genome2, ai_score):
    genome1.fitness += ai_score[0]
    genome2.fitness += ai_score[1]

def eval_genomes(genomes, config):
    pygame.init()
    width, height = 400,400
    screen = pygame.display.set_mode((width,height))
    pygame.display.set_caption("Pong_training_ai!")

    for i, (genome_id1, genome1) in enumerate(genomes):
        if i == len(genomes) -1:
            break
        genome1.fitness = 0
        for genome_id2, genome2 in genomes[i+1:]:
            genome2.fitness = 0 if genome2.fitness == None else genome2.fitness
            train_ai(screen, genome1, genome2, config)

def run_neat(config):
    # p = neat.Checkpointer.restore_checkpoint('neat-checkpoint-x') #x - number of checkpoint reached
    p = neat.Population(config)
    p.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    p.add_reporter(stats)
    #checkpoint after 1 generation
    p.add_reporter(neat.Checkpointer(1))
    #50 is max gen number
    winner = p.run(eval_genomes, 50)
    with open("best.pickle", 'wb') as f:
        pickle.dump(winner, f)

if __name__ == "__main__":
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, "neat_conf.txt")

    config = neat.Config(neat.DefaultGenome, neat.DefaultReproduction,neat.DefaultSpeciesSet, neat.DefaultStagnation,config_path)

    # run_neat(config) #TRAIN AI
    # play_against_ai(config)
    # play_against_another_player()
