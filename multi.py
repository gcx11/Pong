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
from event import *
from color import *

pygame.init()

class EndMultiException(Exception): pass

class MultiPlayer: 

    def __init__(self):
        game.level = 0
        self.label_game_name = Label(0, 0, 800,50,
                                     "THE PONG GAME - MULTIPLAYER".format(game.level),
                                     color.gray, color.black, "courier", 50)
        self.label_game_score = Label(0, 550, 800, 50,
                                      "{0} : {1}".format(score.p1, score.p2),
                                      color.gray, color.black, "arial", 50)
        storage.reset_bricks()
        storage.reset_balls()
        storage.add_ball(Ball(400, 300, 20, 5, 5, 1, 0.005, color.white))
        self.paddle_1 = Paddle(0, 225, 20, 120, 5)
        self.paddle_2 = Paddle(780, 225, 20, 120, 5)
        self.pause = False
        self._running = True

    def __call__(self):
        game.level = 1
        for ball_obj in storage.balls:
            ball_obj.reset()
        storage.reset_bricks()
        self.paddle_1.reset()
        self.paddle_2.reset()
        #levels
        if game.level == 1: # basic
            self.paddle_1.set_speed(5)
            self.paddle_2.set_speed(5)
            for ball_obj in storage.balls:
                ball_obj.acc = 5 * 60 / (game.fps * 1000)
        while self._running:
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == KEYDOWN:
                    if event.key == ord("p"):
                        self.pause = not self.pause
                    if event.key == ord("w") and not self.pause:
                        self.paddle_1.set(-1)
                    if event.key == ord("s") and not self.pause:
                        self.paddle_1.set(1)
                    if event.key == pygame.K_UP and not self.pause:
                        self.paddle_2.set(-1)
                    if event.key == pygame.K_DOWN and not self.pause:
                        self.paddle_2.set(1)
                if event.type == KEYUP:
                    if (event.key == ord("w") and self.paddle_1.get() == -1
                        and not self.pause):
                        self.paddle_1.set(0)
                    if (event.key == ord("s") and self.paddle_1.get() == 1
                        and not self.pause):
                        self.paddle_1.set(0)
                    if (event.key == pygame.K_UP and self.paddle_2.get() == -1
                        and not self.pause):
                        self.paddle_2.set(0)
                    if (event.key == pygame.K_DOWN and self.paddle_2.get() == 1
                        and not self.pause):
                        self.paddle_2.set(0)
            if not self.pause:
                self.raise_events()
                game.screen.fill(color.black)
                self.game_move()
                self.game_collide()
                self.game_draw()
                for ball_obj in storage.balls:
                    ball_obj.accelerate()
                self.game_out()
            pygame.display.update()
            game.fps_clock.tick(game.fps)


    def raise_events(self):
        for ball_obj in storage.balls:
            event.event_paddle(ball_obj, self.paddle_1, self.paddle_2)


    def enemy_play(self):
        max_x = 0
        for ball_obj in storage.balls:
            if ball_obj.x >= max_x:
                max_x = ball_obj.x
                self.paddle_2.set(ai.play(ball_obj, self.paddle_2))

    def me_play(self):
        min_x = game.windowwidth
        for ball_obj in storage.balls:
            if ball_obj.x <= min_x:
                min_x = ball_obj.x
                self.paddle_1.set(ai.play(ball_obj, self.paddle_1))

    def game_collide(self):
        self.paddle_1.collide(self.label_game_name.height,
                              self.label_game_score.height)
        self.paddle_2.collide(self.label_game_name.height,
                              self.label_game_score.height)
        for ball_obj in storage.balls:
            ball_obj.collide(self.label_game_name.height,
                             self.label_game_score.height)
            ball_obj.paddles(self.paddle_1, self.paddle_2)
            for brick_obj in storage.bricks:
                ball_obj.collide_brick(brick_obj)

    def game_move(self):
        self.paddle_1.move()
        self.paddle_2.move()
        for ball_obj in storage.balls:
            ball_obj.move()

    def game_draw(self):
        self.label_game_name.text = "THE PONG GAME - MULTIPLAYER".format(game.level)
        self.label_game_name.draw()
        self.label_game_score.text = "{0} : {1}".format(score.p1, score.p2)
        self.label_game_score.draw()
        for ball_obj in storage.balls:
            ball_obj.draw()
        for brick_obj in storage.bricks:
            brick_obj.draw()
        self.paddle_1.draw()
        self.paddle_2.draw()

    def game_out(self):
        for ball_obj in storage.balls:
            if ball_obj.x <= 0:
                score.add_p2()
                if score.p2 >= game.max_count:
                    score.reset()
                    self.paddle_1.reset()
                    self.paddle_2.reset()
                    storage.reset_bricks()
                    storage.reset_balls()
                    raise EndMultiException
                for ball_obj in storage.balls:
                    ball_obj.reset()
                self.paddle_1.reset()
                self.paddle_2.reset()
            elif ball_obj.x > game.windowwidth:
                score.add_p1()
                for ball_obj in storage.balls:
                    ball_obj.reset()
                self.paddle_1.reset()
                self.paddle_2.reset()
            else:
                pass
            if score.p1 >= game.max_count:
                score.add_score()
                score.reset()
                self.paddle_1.reset()
                self.paddle_2.reset()
                raise EndMultiException
