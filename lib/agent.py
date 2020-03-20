import pygame
import time
import neat
import agentConnect


def eval_genomes(genomes, config):
    for genome_id, genome in genomes:

        net = neat.nn.recurrent.RecurrentNetwork.create(genome, config)
        currentMaxFitness = 0
        currentFitness = 0
        counter = 0

        done = False

        while not done:
            screen = agentConnect.getScreen()
            nnOutput = net.activate(screen)
            agentConnect.outputToControl(nnOutput)
            currentFitness = agentConnect.getFitness()

            if currentFitness > currentMaxFitness:
                currentMaxFitness = currentFitness
                counter = 0
            else:
                counter += 1

            if currentFitness == 10 or counter >= 250:
                done = True
                print(genome_id, currentFitness)

def start():
    config = neat.Config(neat.DefaultGenome, neat.DefaultReproduction,
                         neat.DefaultSpeciesSet, neat.DefaultStagnation,
                         'config-feedforward')
    p = neat.Population(config)

    p.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    p.add_reporter(stats)
    p.add_reporter(neat.Checkpointer(10))

    winner = p.run(eval_genomes, 50)

