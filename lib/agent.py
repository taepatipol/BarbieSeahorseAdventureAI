import pygame
import time
import neat
from agentConnect import AgentConnect

global config
global p

class Agent:
    def __init__(self,agentCon):
        self.agentCon = agentCon

    def eval_genomes(self, genomes, config):
        for genome_id, genome in genomes:
            # restart level
            net = neat.nn.recurrent.RecurrentNetwork.create(genome, config)

            gameEnd = False

            while not gameEnd:
                pass


    def start(self):
        config = neat.Config(neat.DefaultGenome, neat.DefaultReproduction,
                             neat.DefaultSpeciesSet, neat.DefaultStagnation,
                             'config-feedforward')
        p = neat.Population(config)

        p.add_reporter(neat.StdOutReporter(True))
        stats = neat.StatisticsReporter()
        p.add_reporter(stats)
        p.add_reporter(neat.Checkpointer(10))

        evalF = self.eval_genomes
        winner = p.run(evalF, 5)

