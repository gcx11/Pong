#!/usr/bin/env python3

import copy
import math
import pygame
import random
import sys
from pygame.locals import *
from game import *
from mouse import *

pygame.init()

class Label:
    """
    Class for creating labels with text.
    Provides no collisions.
    """


    __slots__ = ("posx", "posy", "width", "height", "text",
                 "bcolor", "fcolor", "font_name", "font_size", "font")

    def __init__(self, posx, posy, width, height, text,
                 bcolor, fcolor, font_name, font_size):
        """
        posx - position on x axis
        posy - position on y axis
        width - width of label
        height - height of label
        text - displayed text
        bcolor - color of brick
        fcolor - color of text
        font_name - name of font
        font_size - size of font
        """
        self.posx = posx
        self.posy = posy
        self.width = width
        self.height = height
        self.text = text
        self.bcolor = bcolor
        self.fcolor = fcolor
        self.font_name = font_name
        self.font_size = font_size
        #checking font
        if self.font_name in pygame.font.get_fonts():
            self.font = pygame.font.SysFont(self.font_name, self.font_size)
        else:
            self.font = pygame.font.SysFont("arial", self.font_size)

    def draw(self):
        """
        It draws label.
        """
        rendered_text = self.font.render(self.text, True, self.fcolor, None)
        text_pos = rendered_text.get_rect()
        text_pos.centerx = self.posx + (self.width/2)
        text_pos.centery = self.posy + (self.height/2)
        pygame.draw.rect(game.screen, self.bcolor,
                         (self.posx, self.posy, self.width, self.height))
        game.screen.blit(rendered_text, text_pos)

    @property
    def clicked(self):
        """
        Return True, if label was clicked.
        """
        if (self.posx <= mouse.x <= self.posx + self.width
            and self.posy <= mouse.y <= self.posy + self.height):
            return True
        else:
            return False
