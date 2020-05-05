'''Game main module.

Contains the entry point used by the run_game.py script.

Feel free to put all your game code here, or in other modules in this "lib"
directory.
'''

import sys
import os

import pygame
from pygame.locals import *

from pgu import timer
from pgu import engine

from cnst import *
import data
import menu
import level
import neat
import pickle
import numpy as np
from use_genome import loadWinner

from agentConnect import AgentConnect
global levelName
global fname
global bestFitness
global AGENT_ACTIVE
global FNAME
global WORKER_NUM

AGENT_ACTIVE = 1 # 2 is using trained genome
GENOME_SAVE_NAME = 'winnerLevel0.pkl'
GENOME_LOAD_NAME = 'winner.pkl'

USING_CHECKPOINT = 0
FILE_PREFIX = 'checkpoint-level1-'
runFile = 'resume-1843'
WORKER_NUM = 20
DUMMY_SCREEN = 1

MENU_ACTIVE = 0 # for no agent
FNAME = 'data/levels/test.tga'



#GPU running
#from numba import jit, cuda
import os

class Input:
    def __init__(self):
        self.up = False
        self.down = False
        self.left = False
        self.right = False
        
class Sound:
    def __init__(self,fname):
        self.sound = None
        if pygame.mixer.get_init():
            try:
                self.sound = pygame.mixer.Sound(fname)
            except:
                pass

    def play(self):
        if self.sound:
            self.sound.stop()
            self.sound.play()

class Game(engine.Game):
    def init_play(self):
        self.score = 0
        self.high = 0
        self.lives = 99
        self.coins = 0
        self.powerup = False
        
    def init(self):
        self.random = 0
        
        self.init_play()
        self.lcur = 0

        if AGENT_ACTIVE == 1 or AGENT_ACTIVE == 2:
            self.agentCon = AgentConnect(self.state)

        self.scale2x = SCALE2X
        if '-scale2x' in sys.argv:
            self.scale2x = not self.scale2x

        sw,sh = SW,SH
        if self.scale2x: sw,sh = sw*2,sh*2
        mode = RESIZABLE #MYCODE
        if '-full' in sys.argv:
            mode ^= FULLSCREEN
        self.screen = pygame.display.set_mode((sw,sh),mode)
        pygame.display.set_caption(TITLE)
        #self.timer = timer.Timer(FPS)
        self.timer = timer.Timer(FPS)
        #self.timer = timer.Speedometer()

        pygame.joystick.init()
        joy_count = pygame.joystick.get_count()
        for joynum in range(joy_count):
            joystick = pygame.joystick.Joystick(joynum)
            joystick.init()
            
        self.input = Input()
        
        if self.scale2x:
            self._screen = self.screen
            self.screen = self._screen.convert().subsurface(0,0,SW,SH)
            
        pygame.font.init()
        
        self.fonts = {}
        self.fonts['intro'] = pygame.font.Font(data.filepath(os.path.join('fonts','LESSERCO.ttf')),36)
        self.fonts['intro2'] = pygame.font.Font(data.filepath(os.path.join('fonts','vectroid.ttf')),72)

        self.fonts['title'] = pygame.font.Font(data.filepath(os.path.join('fonts','vectroid.ttf')),32)
        self.fonts['help'] = pygame.font.Font(data.filepath(os.path.join('fonts','LESSERCO.ttf')),24)
        
        self.font = self.fonts['menu'] = pygame.font.Font(data.filepath(os.path.join('fonts','LESSERCO.ttf')),24)
        
        self.fonts['level'] = pygame.font.Font(data.filepath(os.path.join('fonts','LESSERCO.ttf')),24)
        
        self.fonts['pause'] = pygame.font.Font(data.filepath(os.path.join('fonts','LESSERCO.ttf')),36)
        
        import level
        level.pre_load() #MYCOMMENT
        
        try:
            
            
            if '-nosound' in sys.argv: 1/0
            
            # stop crackling sound on some windows XP machines.
            if os.name == 'posix' or 1:
                try:
                    pygame.mixer.pre_init(44100,-16,2, 1024*3)
                except:
                    pygame.mixer.pre_init()
            else:
                pygame.mixer.pre_init()

            
            pygame.mixer.init()
        except:
            pass
            #print 'mixer not initialized'
        
        self._music_name = None
        
        self.sfx = {}
        for name in ['bubble','capsule','coin','hit','item','powerup',
            'pop','jump','explode','door','fally','boss_explode']:
            self.sfx[name] = Sound(data.filepath(os.path.join('sfx','%s.wav'%name)))
        
    def tick(self):
        r = self.timer.tick()
        if r != None: print r
        
    def flip(self):
        if self.scale2x:
            # test version of pygame ..
            # if 1.8.x
            # pygame.transform.scale(self.screen,(SW*2,SH*2),self._screen)
            # else
            tmp = pygame.transform.scale(self.screen,(SW*2,SH*2))
            self._screen.blit(tmp,(0,0))
            
            # silly TV effect ...
            if '-tv' in sys.argv:
                for y in xrange(0,SH*2,2):
                    self._screen.fill((0,0,0),(0,y,SW*2,1))
            
        pygame.display.flip()
        
    def music_play(self,name,n=-1):
        if self._music_name == name: return
        self._music_name = name
        
        if not pygame.mixer.get_init(): return
        
        for ext in ['wav','ogg']:
            fname = data.filepath(os.path.join('music','%s.%s'%(name,ext)))
            ok = False
            try:
                #print fname
                pygame.mixer.music.load(fname)
                if len(name) == 1 or name == 'death':
                    pygame.mixer.music.set_volume(0.4)
                elif name == 'lvlwin':
                    pygame.mixer.music.set_volume(0.6)
                else:
                    pygame.mixer.music.set_volume(0.65)
                pygame.mixer.music.play(n)
                ok = True
            except:
                #import traceback; traceback.print_exc()
                pass
            if ok: break
        
    def event(self,e):
        # The keys, buttons and axis for the input can be changed in cnst.py

        self.random += 1 + self.random % 100 # this will generate pseudo random numbers

        event = None
        action = None
        if (e.type == KEYDOWN and e.key in JUMP_KEYS) or \
           (e.type == JOYBUTTONDOWN and e.button in JUMP_BUTTONS):
            action = 'jump'
        elif (e.type == KEYUP and e.key in JUMP_KEYS) or \
             (e.type == JOYBUTTONUP and e.button in JUMP_BUTTONS):
            action = 'stop-jump'
        elif e.type == KEYDOWN and e.key in BUBBLE_KEYS or \
            (e.type == JOYBUTTONDOWN and e.button in BUBBLE_BUTTONS):
            action = 'bubble'
        elif e.type == KEYDOWN or e.type == KEYUP:
            if e.type == KEYDOWN:
                value = True
            else:
                value = False
            if e.key in LEFT_KEYS:
                self.input.left = value
                action = 'left'
            if e.key in RIGHT_KEYS:
                self.input.right = value
                action = 'right'
            if e.key in UP_KEYS:
                self.input.up = value
                action = 'up'
            if e.key in DOWN_KEYS:
                self.input.down = value
                action = 'down'
            if e.type == KEYUP:
                action = None
        elif e.type == JOYAXISMOTION:
            if e.axis in HORIZONTAL_AXIS:
                if e.value < -0.6:
                    action = 'left'
                    self.input.left = True
                if e.value > -0.4:
                    self.input.left = False
                if e.value > 0.6:
                    action = 'right'
                    self.input.right = True
                if e.value < 0.4:
                    self.input.right = False
            if e.axis in VERTICAL_AXIS:
                if e.value < -0.6:
                    action = 'up'
                    self.input.up = True
                if e.value > -0.4:
                    self.input.up = False
                if e.value > 0.6:
                    action = 'down'
                    self.input.down = True
                if e.value < 0.4:
                    self.input.down = False
        if e.type is KEYDOWN and e.key in EXIT_KEYS:
            action = 'exit'
        elif e.type is JOYBUTTONDOWN and e.button in EXIT_BUTTONS:
            action = 'exit'
        elif e.type is KEYDOWN and e.key in MENU_KEYS:
            action = 'menu'
        elif e.type is JOYBUTTONDOWN and e.button in MENU_BUTTONS:
            action = 'menu'
        
        if action != None:
            event = pygame.event.Event(USEREVENT, action=action)

            self.fnc('event', event)
            return True
            
        if e.type is QUIT: 
            self.state = engine.Quit(self)
            return 1
        
        #if e.type is KEYDOWN and e.key == K_ESCAPE:
            #self.state = engine.Quit(self)
            #return 1
            
        
        if e.type is KEYDOWN and e.key == K_F4: #K_F12:
            
            try:
                dname = '.'
                if not os.path.exists(dname):
                    return
            except:
                return
            try:
                n = 1
                while n < 1000:
                    fname = os.path.join(dname,'shot%03d.bmp'%n)
                    if not os.path.exists(fname): break
                    n += 1
                self.flip()
                pygame.image.save(self._screen,fname)
                return 1
            except:
                pass
    # Below moved from engine.py ----------------------------------------------------
    def loopStart(self,net=None):
        bestFitness = 0
        if AGENT_ACTIVE == 0:
            self.agentCon = AgentConnect(self.state)
            while not self.quit:
                self.loop()  # MYNOTE here is the first mainloop
                grid = self.agentCon.getScreen()
                #if grid is not None:
                    #print("----------------------------------\n" + "\r" + str(grid))
                fitness = self.agentCon.getFitness()
                if fitness is not None:
                    print fitness
                    if fitness > bestFitness: bestFitness = fitness
                if self.agentCon.getPlayerPos() is not None: print self.agentCon.getPlayerPos()
                if self.agentCon.isGameEnd:
                    break
        if AGENT_ACTIVE == 1 or AGENT_ACTIVE == 2:
            nn = net
            while not self.quit:
                grid = self.agentCon.getScreen().tolist()
                # if grid is not None:
                #     print("----------------------------------\n" + "\r" + str(grid))
                if grid is not None:
                    #input power up status
                    poweredUp = self.agentCon.getPlayerPowerUp()
                    if poweredUp is None or not poweredUp: grid.append(0)
                    else: grid.append(99)
                    move = nn.activate(grid)
                    #print move
                    self.agentCon.outputToControl(move)
                self.loop()
                fitness = self.agentCon.getFitness()
                if fitness is not None:
                    #print fitness
                    if fitness > bestFitness: bestFitness = fitness
                if self.agentCon.getNotImprovedLoop() is not None and self.agentCon.getNotImprovedLoop() >= 1000:
                    break
                if self.agentCon.isGameEnd:
                    #print "a game ended"
                    break

        #print bestFitness
        return bestFitness

    def loop(self):
        s = self.state # default state of Game is Level
        # MYNOTE regular loop without state change fnc will return 0
        if not hasattr(s, '_init') or s._init:
            s._init = 0
            if self.fnc('init'): return
        else:
            if self.fnc('loop'):
                #this will run when transition
                return
        if not hasattr(s, '_paint') or s._paint:
            s._paint = 0
            if self.fnc('paint', self.screen): return
        else:
            if self.fnc('update', self.screen): return

        for e in pygame.event.get():
            # NOTE: this might break API?
            # if self.event(e): return
            if not self.event(e):
                if self.fnc('event', e): return

        # testEvent = pygame.event.Event(USEREVENT,{'action':'right'})
        # pygame.event.post(testEvent)
        self.tick()

        return


class Worker():
    def __init__(self, genome, config):
        self.genome = genome
        self.config = config

    def work(self):
        g = Game()
        l = level.Level(g, FNAME, engine.Quit(g))
        net = neat.nn.recurrent.RecurrentNetwork.create(self.genome, self.config)
        bestFitness = g.run(l, net)  # run in order eval_genomes -> run -> loopStart
        print bestFitness
        return bestFitness

def main():
    #print "Hello from your game's main()"
    #print data.load('sample.txt').read()
    if DUMMY_SCREEN: os.environ["SDL_VIDEODRIVER"] = "dummy"
    
    #fname = None #data.filepath(os.path.join('levels','test.tga'))
    global levelName
    levelName = None
    global fname
    fname = None
    for v in sys.argv:
        if 'lv' in v:
            levelName = v
            
    if AGENT_ACTIVE == 0:
        g = Game()
        g.init()
        l = None
        if MENU_ACTIVE:
            l = l2 = menu.Menu(g)

    #l = menu.Intro(g,l2)

    if levelName != None:
        if levelName == 'lv-j1': fname = 'data/levels/phil_1.tga'
        if levelName == 'lv-j2': fname = 'data/levels/phil_7.tga'
        if levelName == 'lv-j3': fname = 'data/levels/tee_1.tga'
        if levelName == 'lv-j4': fname = 'data/levels/phil_2.tga'
        if levelName == 'lv-v1': fname = 'data/levels/fydo_1.tga'
        if levelName == 'lv-v2': fname = 'data/levels/tim_1.tga'
        if levelName == 'lv-v3': fname = 'data/levels/pekuja_2.tga'
        if levelName == 'lv-b': fname = 'data/levels/phil_8.tga'
        if levelName == 'lv-m1': fname = 'data/levels/pekuja_1.tga'
        if levelName == 'lv-m2': fname = 'data/levels/phil_5.tga'
        if levelName == 'lv-m3': fname = 'data/levels/phil_9.tga'
        if levelName == 'lv-boss': fname = 'data/levels/boss_1.tga'
        if levelName == 'lv-test': fname = 'data/levels/test.tga'
        if AGENT_ACTIVE == 0: l = level.Level(g,fname,engine.Quit(g)) #MYCOMMENT CAN COMMENT THIS AND PLAY GAME LIKE NORMAL
    if AGENT_ACTIVE == 0:
        if l is None:
            l = level.Level(g, FNAME, engine.Quit(g))
        g.run(l)#MYCOMMENT game run menu  !! l is the g.state
    if AGENT_ACTIVE == 1:
        if USING_CHECKPOINT == 0:
            config = neat.Config(neat.DefaultGenome, neat.DefaultReproduction,
                                 neat.DefaultSpeciesSet, neat.DefaultStagnation,
                                 'config-feedforward')
            p = neat.Population(config)
            p.add_reporter(neat.StdOutReporter(True))
            stats = neat.StatisticsReporter()
            p.add_reporter(stats)
            p.add_reporter(neat.Checkpointer(20,filename_prefix=FILE_PREFIX))

        if USING_CHECKPOINT == 1:
            p = neat.Checkpointer.restore_checkpoint(runFile)
            p.add_reporter(neat.StdOutReporter(True))
            stats = neat.StatisticsReporter()
            p.add_reporter(stats)
            p.add_reporter(neat.Checkpointer(20,filename_prefix=FILE_PREFIX))

        pe = neat.ParallelEvaluator(WORKER_NUM, eval_genomes)
        winner = p.run(pe.evaluate, 1000)

        with open(GENOME_SAVE_NAME, 'wb') as output:
            pickle.dump(winner, output, 1)
    if AGENT_ACTIVE == 2:
        net = loadWinner(GENOME_LOAD_NAME)
        g = Game()
        l = level.Level(g, FNAME, engine.Quit(g))
        bestFitness = g.run(l, net)

    print("stop running")

def eval_genomes(genome, config):
    # g = Game()
    # l = level.Level(g, 'data/levels/phil_1.tga', engine.Quit(g))
    # net = neat.nn.recurrent.RecurrentNetwork.create(genome, config)
    # bestFitness = g.run(l,net) # run in order eval_genomes -> run -> loopStart
    # genome.fitness = bestFitness
    aWorker = Worker(genome,config)
    return aWorker.work()

