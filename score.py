#!/usr/bin/env python3

import copy
import math
import pygame
import random
import sys
from pygame.locals import *

pygame.init()

class Score:
    """
    Class for actual score in game.
    """

    __slots__ = ("score", "p1", "p2")

    def __init__(self):
        """
        It sets anything to 0.
        """
        self.p1 = 0
        self.p2 = 0
        self.score = 0

    def reset(self):
        """
        It resets number of goals.
        """
        self.p1 = 0
        self.p2 = 0

    def add_p1(self):
        """
        It adds point to player on left side.
        """
        self.p1 = self.p1 + 1

    def add_p2(self):
        """
        It adds point to player on right side.
        """
        self.p2 = self.p2 + 1

    def add_score(self):
        """
        It counts and add score to player.
        """
        self.score = self.score + self.p1 * (self.p1 - self.p2)

score = Score()
