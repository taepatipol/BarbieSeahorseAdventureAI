"""a state engine. 
"""
import pygame
from pygame.locals import *
import inspect
import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from agentConnect import AgentConnect
import neat


class State:
    """Template Class -- for a state.
    
    <pre>State(game,value...)</pre>
    
    <dl>
    <dt>game<dd>The state engine.
    <dt>value<dd>I usually pass in a custom value to a state
    </dl>
    
    <p>For all of the template methods, they should return None unless they return 
    a new State to switch the engine to.</p>
    """

    def __init__(self, game, value=None):
        self.game, self.value = game, value

    def init(self):
        """Template Method - Initialize the state, called once the first time a state is selected.
        
        <pre>State.init()</pre>
        """
        return

    def paint(self, screen):
        """Template Method - Paint the screen.  Called once after the state is selected.  
        
        <p>State is responsible for calling <tt>pygame.display.flip()</tt> or whatever.</p>
        
        <pre>State.paint(screen)</pre>
        """
        return

    def repaint(self):
        """Template Method - Request a repaint of this state.
        
        <pre>State.repaint()</pre>
        """
        self._paint = 1

    def update(self, screen):
        """Template Method - Update the screen.
        
        <p>State is responsible for calling <tt>pygame.display.update(updates)</tt> or whatever.</p>
        
        <pre>State.update(screen)</pre>
        """
        return

    def loop(self):
        """Template Method - Run a logic loop, called once per frame.
        
        <pre>State.loop()</pre>
        """
        return

    def event(self, e):
        """Template Method - Recieve an event.
        
        <pre>State.event(e)</pre>
        """
        return


class Quit(State):
    """A state to quit the state engine.
    
    <pre>Quit(game,value)</pre>
    """

    def init(self):
        self.game.quit = 1


class Game:
    """Template Class - The state engine.
    """
    def __init__(self):
        self.agentCon = None
        self.agent = None

    def fnc(self, f, v=None): #MYNOTE use to run function f of self.state with v attr
        s = self.state
        if not hasattr(s, f): return 0
        f = getattr(s, f)
        # try:
        if v != None:
            r = f(v)
        else:
            r = f()
        if r != None: #MYNOTE change state to result
            self.state = r
            self.state._paint = 1
            self.agentCon.setLevel(self.state)
            return 1
        # except:
        #    import traceback; traceback.print_exc()

        return 0 #if 1 it will infinite loop with black screen

    def run(self, state, net=None):
        """Run the state engine, this is a infinite loop (until a quit occurs).
        
        <pre>Game.run(state,screen=None)</pre>
        
        <dl>
        <dt>game<dd>a state engine
        <dt>screen<dd>the screen
        </dl>
        """
        self.quit = 0
        self.state = state
        #if screen != None: self.screen = screen

        self.init()

        best = self.loopStart(net)
        #print 'the best fitness: '+ str(best)
        return best

    def init(self):
        """Template Method - called at the beginning of State.run() to initialize things.
        
        <pre>Game.init()</pre>
        """
        return

    def tick(self):
        """Template Method - called once per frame, usually for timer purposes.
        
        <pre>Game.tick()</pre>
        """
        pygame.time.wait(10)

    def event(self, e):
        """Template Method - called with each event, so the engine can capture special events.
        
        <pre>Game.event(e): return captured</pre>
        
        <p>return a True value if the event is captured and does not need to be passed onto the current
        state</p>
        """
        if e.type is QUIT:
            self.state = Quit(self)
            return 1

# vim: set filetype=python sts=4 sw=4 noet si :
