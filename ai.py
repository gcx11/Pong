#!/usr/bin/env python3

import copy
import math
import pygame
import random
import sys
from pygame.locals import *

pygame.init()

class AI():
    """
    Simple AI for paddle.
    It can be used for both paddles.
    """

    def play(self, ball, paddle):
        """
        If it returns 1 -> move up.
        If it returns -1 -> move down.
        If it returns 0 -> don´t move.
        Parameters:
        ball - instance of ball
        paddle - instance of paddle
        """
        if ball.y <= paddle.posy + (paddle.height/4):
            return -1
        elif ball.y >= paddle.posy + 3*(paddle.height/4):
            return 1
        else:
            return 0

ai = AI()
