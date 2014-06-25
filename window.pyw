#!/usr/bin/env python3

import copy
import math
import pygame
import random
import sys
from pygame.locals import *
from game import *
from score import *
from paddle import *
from ball import *
from ai import *
from mouse import *
from label import *
from brick import *
from storage import *
from color import *
from level import *
from multi import *

pygame.init()

class NewGameException(Exception): pass
class MultiPlayerException(Exception): pass
class JumpException(Exception): pass


class Window:

    def __init__(self):
        self._temp = ""
        self._running = True

    def mainloop(self):
        while True:
            self.menu_loop()
            if self._temp == "single":
                score.score = 0
                level = Level()
                while True:
                    try:
                        level()
                    except NextLevelException:
                        self.next_loop()
                    except EndGameException:
                        break
            elif self._temp == "multi":
                score.score = 0
                multiplayer = MultiPlayer()
                while True:
                    try:
                        multiplayer()
                    except EndGameException:
                        break
            else:
                pass

    def menu_loop(self):
        self.label_game_name = Label(50, 50, 700, 75, "THE PONG GAME",
                                     color.black, color.white, "courier", 75)
        self.label_game_singleplayer = Label(50, 150, 700, 100, "Player vs AI",
                                      color.white, color.black, "courier", 50)
        self.label_game_multiplayer = Label(50, 300, 700, 100, "Player vs Player"
                                     , color.white, color.black, "courier", 50)
        self.label_game_exit = Label(50, 450, 700, 100, "Exit Game",
                                     color.white, color.black, "courier", 50)
        try:
            while self._running:
                game.screen.fill(color.black)
                for event in pygame.event.get():
                    if event.type == QUIT:
                        pygame.quit()
                        sys.exit()
                    if event.type == MOUSEBUTTONDOWN:
                        mouse.x , mouse.y = event.dict["pos"]
                        if event.dict["button"] == 1:
                            if self.label_game_singleplayer.clicked:
                                raise NewGameException
                            elif self.label_game_multiplayer.clicked:
                                raise MultiPlayerException
                            elif self.label_game_exit.clicked:
                                pygame.quit()
                                sys.exit()
                            else:
                                pass         
                self.menu_draw()
                pygame.display.update()
                game.fps_clock.tick(game.fps)
        except NewGameException:
            self._temp = "single"
        except MultiPlayerException:
            self._temp = "multi"

    def menu_draw(self):
        self.label_game_name.draw()
        self.label_game_singleplayer.draw()
        self.label_game_multiplayer.draw()
        self.label_game_exit.draw()

    def next_loop(self):
        self.label_next = Label(50, 150, 700, 75, "LEVEL {0} - SCORE {1}".format(game.level, score.score),
                                     color.black, color.white, "courier", 75)
        self.label_click = Label(50, 300, 700, 75, "NEXT",
                                     color.black, color.white, "courier", 75)
        try:
            while True:
                game.screen.fill(color.black)
                for event in pygame.event.get():
                    if event.type == QUIT:
                        pygame.quit()
                        sys.exit()
                    if event.type == MOUSEBUTTONDOWN:
                        mouse.x , mouse.y = event.dict["pos"]
                        if event.dict["button"] == 1:
                            if self.label_click.clicked:
                                raise JumpException
                self.label_next.draw()
                self.label_click.draw()
                pygame.display.update()
                game.fps_clock.tick(game.fps)
        except JumpException:
            pass
        
window = Window()
window.mainloop()
