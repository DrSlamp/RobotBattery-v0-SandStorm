import time

import numpy as np

import gym
from gym import spaces
import pygame

from . import settings
from .window import Window
#from .world import World

class RobotBaterryEnv(gym.Env):
    metadata = {"render_modes": ["human"], "render_fps": 60}

    def __init__(self, *args, **kwargs):
        super().__init__()
        self.action_space = spaces.Discrete(4)
        self.observation_space = spaces.Discrete(16)
        self.current_action = 1
        self.current_state = 0 
        self.current_reward = 0

        self.current_energy = 0
        self.initial_energy = 100
        
        self.delay = settings.DEFAULT_DELAY
        self.P = settings.P

        self.window = Window("R.E SandStorm energy", self.current_state, self.current_action)

    #following Computer Systems: Environments Modeling (ULA VE) - Lecture 2
    
    def reset(self, seed=None, options=None):
        super().reset(seed=seed)
        np.random.seed(seed)

        if options is not None:
            if not isinstance(options, dict):
                raise RuntimeError("Variable options is not a dictionary")
            self.delay = options.get('delay', settings.DEFAULT_DELAY)

        self.current_state = 0
        self.current_action = 1
        self.current_energy = 0
        self.initial_energy = 100

        self.window.reset(self.current_state, self.current_action)
        return 0, {}

    def step(self, action):
            self.current_action = action

            possibilities = self.P[self.current_state][self.current_action]

            p = 0
            i = 0

            r = np.random.random()

            #if np.random.random() < 1 - self.current_energy / self.initial_energy:
              #  self.current_state        


            while r > p:
                r -= p
                p, self.current_state, self.current_reward, terminated = possibilities[i]
                i += 1
                
            self.window.update(
                self.current_state,
                self.current_action,
                self.current_reward,
                terminated

            )

            self.render()
            time.sleep(self.delay)
            
            return self.current_state, self.current_reward, terminated, False,  {}
    
    def render(self):
        self.window.render()

    def close(self):
        self.window.close()


       # if np.random.random() < 1 - current_energy / initial_energy:
    # Elegir quedarse en la misma posición o ir a una diferente a la elegida por la acción
#else:
    # Ir a la dirección esperada por la acción


   
  
