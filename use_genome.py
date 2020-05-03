import pickle
import neat

def loadWinner():
    file = open('winner.pkl','rb')
    genome = pickle.load(file)
    file.close()

    #print('\nBest genome:\n{!s}'.format(genome))

    config = neat.Config(neat.DefaultGenome, neat.DefaultReproduction,
                         neat.DefaultSpeciesSet, neat.DefaultStagnation,
                         'config-feedforward')
    net = neat.nn.FeedForwardNetwork.create(genome, config)

    #print('\nBest nn:\n{!s}'.format(net))
    return net



if __name__ == '__main__':
    loadWinner()