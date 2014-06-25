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

class NextLevelException(Exception): pass
class EndGameException(Exception): pass

class Level:
    

    def __init__(self):
        game.level = 0
        self.label_game_name = Label(0, 0, 800,50,
                                     "THE PONG GAME - LEVEL {0}".format(game.level),
                                     color.gray, color.black, "courier", 50)
        self.label_game_score = Label(0, 550, 800, 50,
                                      "{0} : {1}".format(score.p1, score.p2),
                                      color.gray, color.black, "arial", 50)
        storage.reset_bricks()
        storage.reset_balls()
        self.ball_1 = Ball(400, 300, 20, 5, 5, 1, 0.005, color.white)
        #self.ball_2 = Ball(400, 300, 20, 5, 5, 1, 0.005, color.white)
        storage.add_ball(self.ball_1)
        #storage.add_ball(self.ball_2)
        self.paddle_1 = Paddle(0, 225, 20, 120, 5)
        self.paddle_2 = Paddle(780, 225, 20, 120, 5)
        self.pause = False
        self._running = True

    def __call__(self):
        game.level = game.level + 1
        for ball_obj in storage.balls:
            ball_obj.reset()
        storage.reset_bricks()
        self.paddle_1.reset()
        self.paddle_2.reset()
        #levels
        if game.level == 1: # basic
            self.paddle_1.set_speed(5)
            self.paddle_2.set_speed(1)
            for ball_obj in storage.balls:
                ball_obj.acc = 1 * 60 / (game.fps * 1000)
        elif game.level == 2: # judge
            self.paddle_1.set_speed(5)
            self.paddle_2.set_speed(2)
            for ball_obj in storage.balls:
                ball_obj.acc = 3 * 60 / (game.fps * 1000)
            storage.add_brick(Brick(250, 250, 100, 100, 0))
            storage.add_brick(Brick(450, 250, 100, 100, 0))
        elif game.level == 3: # half
            self.paddle_1.set_speed(5)
            self.paddle_2.set_speed(2)
            for ball_obj in storage.balls:
                ball_obj.acc = 3 * 60 / (game.fps * 1000)
            storage.add_brick(Brick(200, 150, 100, 100, 0))
            storage.add_brick(Brick(500, 150, 100, 100, 1))
            storage.add_brick(Brick(500, 350, 100, 100, 0))
            storage.add_brick(Brick(200, 350, 100, 100, 1))
        elif game.level == 4: # demolition
            self.paddle_1.set_speed(5)
            self.paddle_2.set_speed(2)
            for ball_obj in storage.balls:
                ball_obj.acc = 3 * 60 / (game.fps * 1000)
            for i in range(14):
                for j in range(10):
                    storage.add_brick(Brick(50*(i + 1), 50*(j + 1),
                                            50, 50, 1))
        elif game.level == 5: # hot and cold
            self.paddle_1.set_speed(5)
            self.paddle_2.set_speed(2)
            for ball_obj in storage.balls:
                ball_obj.acc = 3 * 60 / (game.fps * 1000)
            storage.add_brick(Brick(350, 150, 100, 100, 2))
            storage.add_brick(Brick(350, 350, 100, 100, 3))
        elif game.level == 6: # defence
            self.paddle_1.set_speed(5)
            self.paddle_2.set_speed(5)
            for ball_obj in storage.balls:
                ball_obj.acc = 6 * 60 / (game.fps * 1000)
            storage.add_brick(Brick(50, 50, 100, 100, 0))
            storage.add_brick(Brick(50, 250, 100, 100, 0))
            storage.add_brick(Brick(50, 450, 100, 100, 0))
            storage.add_brick(Brick(50, 650, 100, 100, 0))
        elif game.level == 7: # small
            self.paddle_1 = Paddle(0, 225, 20, 60, 5)
            self.paddle_2 = Paddle(780, 225, 20, 60, 5)
            self.paddle_1.set_speed(5)
            self.paddle_2.set_speed(2)
            for ball_obj in storage.balls:
                ball_obj.acc = 3 * 60 / (game.fps * 1000)
            for i in range(3):
                for j in range(10):
                    storage.add_brick(Brick(100 + i*100, 50*(j + 1),
                                            50, 50, 1))
                    storage.add_brick(Brick(650 - i*100, 50*(j + 1),
                                            50, 50, 1))
        elif game.level == 8: # nothing
            self.paddle_1.set_speed(5)
            self.paddle_2.set_speed(2)
            for ball_obj in storage.balls:
                ball_obj.acc = 3 * 60 / (game.fps * 1000)
            storage.add_brick(Brick(50, 50, 100, 100, 4))
        else: #stuff
            self.paddle_1.set_speed(5)
            self.paddle_2.set_speed(20)
            storage.add_brick(Brick(200, 150, 100, 100, 0))
            storage.add_brick(Brick(600, 150, 100, 100, 0))
            storage.add_brick(Brick(600, 450, 100, 100, 0))
            storage.add_brick(Brick(200, 450, 100, 100, 0))
            for ball_obj in storage.balls:
                ball_obj.acc = 0.005
        # levels end
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
                    if event.key == ord("h") and not self.pause:
                        score.add_p1()
                if event.type == KEYUP:
                    if (event.key == ord("w") and self.paddle_1.get() == -1
                        and not self.pause):
                        self.paddle_1.set(0)
                    if (event.key == ord("s") and self.paddle_1.get() == 1
                        and not self.pause):
                        self.paddle_1.set(0)
            if not self.pause:
                self.raise_events()
                self.enemy_play()
                #self.me_play()
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
        self.label_game_name.text = "THE PONG GAME - LEVEL {0}".format(game.level)
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
                    raise EndGameException
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
                raise NextLevelException
