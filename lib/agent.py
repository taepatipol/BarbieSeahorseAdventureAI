import pygame
import time
import neat
import agentConnect


def eval_genomes(genomes, config):
    for genome_id, genome in genomes:

        net = neat.nn.recurrent.RecurrentNetwork.create(genome, config)
        currentMaxFitness = 0
        currentFitness = 0

        done = False

        while not done:
            done = True

def start(self):
    config = neat.Config(neat.DefaultGenome, neat.DefaultReproduction,
                         neat.DefaultSpeciesSet, neat.DefaultStagnation,
                         'config-feedforward')
    p = neat.Population(config)

    p.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    p.add_reporter(stats)
    p.add_reporter(neat.Checkpointer(10))

    winner = p.run(eval_genomes, 50)

