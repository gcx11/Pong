#!/usr/bin/env python3

import copy
import math
import pygame
import random
import sys
from pygame.locals import *
from game import *

pygame.init()

class Game:

    def __init__(self, windowwidth, windowheight, fps):
        """
        Basic setting for game.
        Parametrs:
        window width, window height, FPS
        """
        self.fps_clock = pygame.time.Clock()
        self.windowwidth = windowwidth
        self.windowheight = windowheight
        self.fps = fps
        self.screen = pygame.display.set_mode((self.windowwidth,
                                              self.windowheight))
        pygame.display.set_caption("Pong")
        self.level = 1
        self.max_count = 5

game = Game(800, 600, 240)


