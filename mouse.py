#!/usr/bin/env python3

import copy
import math
import pygame
import random
import sys
from pygame.locals import *

pygame.init()

class Mouse:
    """
    Class mouse position.
    """
    __slots__ = ("x", "y")

    def __init__(self):
        """
        It sets mouse position on (0, 0).
        """
        self.x = 0
        self.y = 0

mouse = Mouse()
