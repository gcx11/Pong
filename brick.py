#!/usr/bin/env python3

import copy
import math
import pygame
import random
import sys
from pygame.locals import *
from game import *
from color import *

pygame.init()

class Brick:

    __slots__ = ("posx", "posy", "width", "height", "bcolor", "event_type")

    def __init__(self, posx, posy, width, height, event_type = 0):
        """
        Parametrs:
        posx - position on x axis
        posy - position on y axis
        width - width of brick
        height - height of brick
        bcolor - color of brick
        """
        self.posx = posx
        self.posy = posy
        self.width = width
        self.height = height
        if event_type == 0 or event_type == 1:
            self.bcolor = color.gray
        elif event_type == 2:
            self.bcolor = color.turquoise
        elif event_type == 3:
            self.bcolor = color.orangered
        elif event_type == 4:
            self.bcolor = color.green
        elif event_type == 5:
            self.bcolor = color.yellow
        self.event_type = event_type

    def draw(self):
        """
        It draws brick.
        """
        pygame.draw.rect(game.screen, self.bcolor,
                         (self.posx, self.posy, self.width, self.height))
