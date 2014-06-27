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

class Paddle():

    """
    __slots__ = ("old_posx", "old_posy", "posx", "posy", "width", "height",
                 "speed", "def_speed", "direction", "freezed", "bursted")
    """

    def __init__(self, posx, posy, width, height, speed, freezed = False,
                 bursted = False, confused = False):
        """
        Parameters:
        posx - position on x axis
        posy - position on y axis
        width - width of label
        height - height of label
        """
        self.old_posx = posx
        self.old_posy = posy
        self.posx = posx
        self.posy = posy
        self.width = width
        self.height = height
        self.speed = speed
        self.def_speed = speed
        self.direction = 0
        self.freezed = freezed
        self.bursted = bursted
        self.confused = confused

    def set(self, value):
        """
        It sets direction.
        1 = up, 0 = nothing, -1 = down
        """
        if value in range(-1, 2):
            self.direction = value

    def get(self):
        """
        It returns direction.
        """
        return self.direction

    def move(self):
        """
        It moves with paddle.
        """
        self.posy = self.posy + self.speed * self.direction * 60 / game.fps

    def set_speed(self, value):
        self.def_speed = value
        self.speed = value

    def reset(self):
        """
        It resets paddle stats.
        """
        self.posx = copy.deepcopy(self.old_posx)
        self.posy = copy.deepcopy(self.old_posy)
        self.speed = self.def_speed
        self.freezed = False
        self.bursted = False
        self.confused = False
        self.direction = 0

    def collide(self, up, down):
        """
        It provides collision with label.
        Parameters:
        up - instance of upper label
        down - instance of bottom label
        """
        if self.posy < up:
            self.posy = up
            self.direction = 0
        elif self.posy > game.windowheight - self.height - down:
            self.posy = game.windowheight - self.height - down
            self.direction = 0
        else:
            pass

    def freeze(self):
        if self.freezed:
            pass
        else:
            if self.bursted:
                self.speed = self.def_speed
                self.freezed = False
                self.bursted = False
            else:
                self.speed = self.speed / 2
                self.freezed = True

    def burst(self):
        if self.bursted:
            pass
        else:
            if self.freezed:
                self.speed = self.def_speed
                self.freezed = False
                self.bursted = False
            else:
                self.speed = self.speed * 2
                self.bursted = True

    def confuse(self):
        if self.confused:
            pass
        else:
            self.confused = True

    def heal(self):
        if self.confused:
            self.confused = False
        else:
            pass

    def draw(self):
        """
        It draws paddle.
        """
        if self.freezed == True:
            self.color = color.turquoise
        elif self.bursted == True:
            self.color = color.orangered
        else:
            self.color = color.white
        pygame.draw.rect(game.screen, self.color,
                         (self.posx, self.posy, self.width, self.height))
