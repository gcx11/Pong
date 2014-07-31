#!/usr/bin/env python3

import copy
import math
import pygame
import random
import sys
import time
from pygame.locals import *

pygame.init()

class Timer():
    """
    Simple Timer.
    """

    __slots__ = ("_running", "time", "seconds")

    def __init__(self):
        self._running = False
        self.time = 0
        self.seconds = 0

    def start(self, seconds):
        """
        Start timer.
        Parameters:
        seconds - time in seconds
        """
        self.seconds = seconds
        if self._running == False:
            self._running = True
            self.time = time.time()

    def check(self):
        """
        Return True, if time is over.
        Else return False.
        """
        if time.time() - self.time >= self.seconds:
            self._running = False
            return True
        else:
            return False
    

my_timer = Timer()
