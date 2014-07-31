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
from timer import *
from color import *
from level import *
from multi import *


pygame.init()

banner = pygame.image.load(r"images/geekwork_splash.png")

#exceptions
class NewGameException(Exception): pass
class MultiPlayerException(Exception): pass
class TutorialException(Exception): pass
class EndTutorialException(Exception): pass
class JumpException(Exception): pass


class Window:
    """
    Main game class.
    """

    def __init__(self):
        self._temp = ""
        self._running = True

    def mainloop(self):
        """
        Game mainloop.
        """
        while True:
            self.banner_loop()
            self.menu_loop()
            if self._temp == "single":
                score.score = 0
                level = Level()
                while True:
                    try:
                        level()
                    except NextLevelException:
                        self.next_loop()
                    except EndSingleException:
                        break
            elif self._temp == "multi":
                score.score = 0
                multiplayer = MultiPlayer()
                while True:
                    try:
                        multiplayer()
                    except EndMultiException:
                        break
            elif self._temp == "tutorial":
                while True:
                    try:
                        self.tutorial_loop()
                    except EndTutorialException:
                        break
            else:
                pass

    def banner_loop(self):
        my_timer.start(7)
        while True:
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
            if my_timer.check():
                break
            game.screen.blit(banner, (0, 0))
            pygame.display.update()
            game.fps_clock.tick(game.fps)

    def menu_loop(self):
        """
        Calls menu loop.
        """
        self.label_game_name = Label(50, 50, 700, 75, "THE PONG GAME",
                                     color.black, color.white, "courier", 75)
        self.label_game_singleplayer = Label(50, 150, 700, 90, "Player vs AI",
                                      color.white, color.black, "courier", 50)
        self.label_game_multiplayer = Label(50, 260, 700, 90, "Player vs Player"
                                     , color.white, color.black, "courier", 50)
        self.label_game_tutorial = Label(50, 370, 700, 90, "How to Play",
                                     color.white, color.black, "courier", 50)
        self.label_game_exit = Label(50, 480, 700, 90, "Exit Game",
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
                            elif self.label_game_tutorial.clicked:
                                raise TutorialException
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
        except TutorialException:
            self._temp = "tutorial"

    def menu_draw(self):
        """
        Draws menu labels.
        """
        self.label_game_name.draw()
        self.label_game_singleplayer.draw()
        self.label_game_multiplayer.draw()
        self.label_game_tutorial.draw()
        self.label_game_exit.draw()

    def next_loop(self):
        """
        Draws score after turn.
        """
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

    def tutorial_loop(self):
        """
        Tutorial loop.
        """
        self.label_text_1 = Label(0, 0, 800, 100,
                                "How To Play",
                                color.black, color.white, "courier", 100)
        self.label_text_2 = Label(0, 100, 800, 75,
                                "Keyboard (move):",
                                color.black, color.white, "courier", 50)
        self.label_text_3 = Label(0, 175, 400, 50,
                                "Player 1 -",
                                color.black, color.white, "courier", 50)
        self.label_text_4 = Label(400, 175, 400, 50,
                                "Player 2 -",
                                color.black, color.white, "courier", 50)
        self.label_text_5 = Label(0, 250, 400, 50,
                                "W - up",
                                color.black, color.white, "courier", 50)
        self.label_text_6 = Label(400, 250, 400, 50,
                                "UP - up",
                                color.black, color.white, "courier", 50)
        self.label_text_7 = Label(0, 325, 400, 50,
                                "S - down",
                                color.black, color.white, "courier", 50)
        self.label_text_8 = Label(400, 325, 400, 50,
                                "DOWN - down",
                                color.black, color.white, "courier", 50)
        self.label_text_9 = Label(0, 400, 800, 50,
                                "P - pause",
                                color.black, color.white, "courier", 50)
        self.label_text_10 = Label(200, 475, 400, 50,
                                "OK",
                                color.white, color.black, "courier", 50)
        while True:
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == MOUSEBUTTONDOWN:
                    mouse.x , mouse.y = event.dict["pos"]
                    if event.dict["button"] == 1:
                        if (self.label_text_10.clicked):
                            raise EndTutorialException
            game.screen.fill(color.black)
            self.tutorial_draw()
            pygame.display.update()
            game.fps_clock.tick(game.fps)

    def tutorial_draw(self):
        """
        Draws tutorial labels.
        """
        self.label_text_1.draw()
        self.label_text_2.draw()
        self.label_text_3.draw()
        self.label_text_4.draw()
        self.label_text_5.draw()
        self.label_text_6.draw()
        self.label_text_7.draw()
        self.label_text_8.draw()
        self.label_text_9.draw()
        self.label_text_10.draw()


#creating window
window = Window()
window.mainloop()
