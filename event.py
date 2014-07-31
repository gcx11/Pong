#!/usr/bin/env python3

import copy
import math
import pygame
import random
import sys
from pygame.locals import *
from storage import *

pygame.init()

class Event:

    def __init__(self):
        pass

    def event_paddle(self, ball, paddle_1, paddle_2):
        if ball.event_type == 2:
            if ball.owner:
                paddle_1.freeze()
            else:
                paddle_2.freeze()
        elif ball.event_type == 3:
            if ball.owner:
                paddle_2.burst()
            else:
                paddle_1.burst()
        elif ball.event_type == 4:
            if ball.owner: 
                paddle_1.confuse()
            else:
                paddle_2.confuse()
        elif ball.event_type == 5:
            if ball.owner: 
                paddle_2.heal()
            else:
                paddle_1.heal()
        ball.event_type = 0

    def event_brick(self, brick, ball):
        if brick.event_type == 1:
            storage.remove_brick(brick)
        elif brick.event_type == 2:
            ball.event_type = 2
        elif brick.event_type == 3:
            ball.event_type = 3
        elif brick.event_type == 4:
            ball.event_type = 4
            
    def event_ball(self, ball):
        if ball.event_type == 1:
            storage.remove_ball(ball)
        

event = Event()
