#!/usr/bin/env python3

import copy
import math
import pygame
import random
import sys
from pygame.locals import *

pygame.init()

class Storage:
    """
    This class storages instances of balls and bricks.
    """

    def __init__(self):
        """
        Create empty lists for bricks and balls.
        """
        self.bricks = []
        self.balls = []
        self.paddles = []

    def add_brick(self, brick):
        """
        Add instance of brick to storage.
        """
        self.bricks.append(brick)

    def add_ball(self, ball):
        """
        Add instance of ball to storage.
        """
        self.balls.append(ball)

    def add_paddle(self, paddle):
        """
        Add instance of paddle to storage.
        """
        self.paddles.append(paddle)

    def reset_bricks(self):
        """
        Delete all bricks from list.
        """
        self.bricks = []

    def reset_balls(self):
        """
        Delete all balls from list.
        """
        self.balls = []

    def remove_brick(self, brick):
        """
        Delete brick from list.
        """
        self.bricks.remove(brick)

    def remove_ball(self, brick):
        """
        Delete ball from list.
        """
        self.balls.remove(ball)

storage = Storage()
