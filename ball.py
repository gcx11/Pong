#!/usr/bin/env python3

import copy
import math
import pygame
import random
import sys
from pygame.locals import *
from game import *
from event import *
from color import *

pygame.init()

class Ball():
    """
    Class for creating ball.
    """

    __slots__ = ("x", "y", "r", "v", "def_v", "angle", "acc", "color",
                 "owner", "event_type")
    
    def __init__(self, x, y, r, v, def_v, angle, acc, color, event_type = 0):
        """
        Parameters:
        x - starning position of x axis
        y - starning position of x axis
        r - radius
        v - velocity
        def_v - minimal velocity of ball
        angle - starting angle
        acc - acceleration
        color - color of ball
        """
        self.x = x
        self.y = y
        self.r = r
        self.v = v
        self.def_v = def_v
        self.angle = 2* math.pi - angle
        self.acc = acc
        self.color = color
        self.owner = random.randint(0, 1)
        self.event_type = event_type
        
    def accelerate(self):
        """
        Accelerate ball.
        """
        self.v = self.v + self.acc * 60 / game.fps
            
    def move(self):
        """
        Move ball on new position.
        """
        self.x = self.x + (self.v * 60 / game.fps * math.cos(self.angle))
        self.y = self.y + (self.v * 60 / game.fps * math.sin(self.angle))

    def reset(self):
        """
        Reset ball stats.
        """
        self.x = game.windowwidth/2
        self.y = game.windowheight/2
        self.v = self.def_v
        self.owner = random.randint(0, 1)
        self.event_type = 0
        
        temp = random.randint(0, 3)
        if temp == 0:
            self.angle = random.randint(1, 49) / 200 * math.pi
        elif temp == 1:
            self.angle = random.randint(141, 199) / 200 * math.pi
        elif temp == 2:
            self.angle = random.randint(201, 249) / 200 * math.pi
        else:
            self.angle = random.randint(351, 399) / 200 * math.pi
        
    def collide(self, up, down):
        """
        Collide with labels.
        Parameters:
        up - height of upper label
        down - height of bottom label
        """
        #next stats
        _angle = copy.deepcopy(self.angle)
        _v = copy.deepcopy(self.v)
        _x = self.x + ((_v + self.acc * 60 / game.fps) * 60 / game.fps * math.cos(_angle))
        _y = self.y + ((_v + self.acc * 60 / game.fps) * 60 / game.fps * math.sin(_angle))
        
        if(_y <= up or _y + self.r >= game.windowheight - down):
            self.angle = 2 * math.pi - self.angle
            # bit of randomness
            self.angle = (self.angle +
                          (math.pi / 1000 * (random.randint(-40, 40))))
        else:
            pass

    def collide_brick(self, brick):
        """
        Collision with brick.
        Parameters:
        brick - instance of brick
        """
        _angle = copy.deepcopy(self.angle)
        _v = copy.deepcopy(self.v)
        _x = self.x + ((_v + self.acc * 60 / game.fps) * 60 / game.fps * math.cos(_angle))
        _y = self.y + ((_v + self.acc * 60 / game.fps) * 60 / game.fps * math.sin(_angle))
        _delta_x = _x - (brick.posx + brick.width/2)
        _delta_y = _y - (brick.posy + brick.height/2)
        
        if (self.check_collision(brick)):
            angle = math.atan2(_delta_y,_delta_x)
            angle = 2*math.pi - angle
            while ((angle < 0) or (angle >= 2*math.pi)):
                if angle < 0:
                   angle = angle + 2*math.pi
                else:
                   angle = angle - 2*math.pi

            # !?! - bad bug fix - weird collision between
            # ball and brick, ball stuck in brick
            if ((brick.posx <= self.x <= brick.posx + brick.width) and
                (brick.posy <= self.y <= brick.posy + brick.height)):
                self.x = game.windowwidth/2
                self.y = game.windowheight/2

                
            if ((0 <= angle <= math.pi/4) or
                (3*math.pi/4 <= angle <= 5*math.pi/4) or
                (7*math.pi/4 <= angle <= 2*math.pi)):
                self.angle = 3*math.pi - self.angle
                # bit of randomness
                self.angle = (self.angle +
                              (math.pi / 1000 * (random.randint(-40, 40))))
            else:
                self.angle = 2*math.pi - self.angle
                # bit of randomness
                self.angle = (self.angle +
                              (math.pi / 1000 * (random.randint(-40, 40))))

            #raise event
            event.event_brick(brick, self)

    def check_collision(self, brick):
        """
        Returns True, if ball collide with brick.
        Else returns False.
        """
        _angle = copy.deepcopy(self.angle)
        _v = copy.deepcopy(self.v)
        _x = self.x + ((_v + self.acc * 60 / game.fps)
                       * 60 / game.fps * math.cos(_angle))
        _y = self.y + ((_v + self.acc * 60 / game.fps)
                       * 60 / game.fps * math.sin(_angle))


        """
        directions = ((1, 0), (0, 1), (-1, 0), (0, 1),
                      (0.71, 0.71), (-0.71, 0.71), 
                      (-0.71, -0.71), (0.71, -0.71), 
                      (0, 0))
        """
        """
                      ((0.5, 0.86), (0.86, 0.5),
                      (-0.5, -0.86), (-0.86, -0.5), 
                      (-0.5, 0.86), (-0.86, 0.5),  
                      (0.5, -0.86), (0.86, -0.5))
        """
        """
        for a, b in directions:
            if ((brick.posx <= _x + a*self.r <= brick.posx + brick.width + a*self.r)
                and
                (brick.posy <= _y + b*self.r <= brick.posy + brick.height + b*self.r)):
                return True
        else:
            return False
        """
        #http://stackoverflow.com/questions/401847/
        #circle-rectangle-collision-detection-intersection
        _x = _x + self.r/2
        _y = _y + self.r/2

        _brick_x = brick.posx + brick.width/2
        _brick_y = brick.posy + brick.height/2

        cd_x = abs(_x - _brick_x)
        cd_y = abs(_y - _brick_y)

        if cd_x > brick.width/2 + self.r/2:
            return False
        if cd_y > brick.height/2 + self.r/2:
            return False

        if cd_x <= brick.width/2:
            return True
        if cd_y <= brick.height/2:
            return True

        cd_sq = ((cd_x - brick.width/2)*(cd_x - brick.width/2) -
                 (cd_y - brick.height/2)*(cd_y - brick.height/2))

        return (cd_sq <= (self.r*self.r/4))
        
                    

    def paddles(self, paddle_1, paddle_2):
        """
        Collide with paddles.
        Parameters:
        paddle_1 - left paddle
        paddle_2 - right paddle
        """
        #next stats
        _angle = copy.deepcopy(self.angle)
        _v = copy.deepcopy(self.v)
        _x = self.x + ((_v + self.acc * 60 / game.fps) * 60 / game.fps * math.cos(_angle))
        _y = self.y + ((_v + self.acc * 60 / game.fps) * 60 / game.fps * math.sin(_angle))
        
        if ((_x <= paddle_1.width) and
            (paddle_1.posy - self.r <= _y <= paddle_1.posy +
             paddle_1.height + self.r)):
            self.angle = 3 * math.pi - self.angle
            self.angle = (self.angle + math.pi / 1000 *
                          (self.y - paddle_1.posy - paddle_1.height/2))
            self.owner = 0
                    
        if ((_x + self.r >= game.windowwidth - paddle_2.width) and
            (paddle_2.posy - self.r <= _y <= paddle_2.posy +
             paddle_2.height + self.r)):
            self.angle = 3 * math.pi - self.angle
            self.angle = (self.angle + math.pi / 1000 *
                          (self.y - paddle_2.posy - paddle_2.height/2))
            self.owner = 1
        
    def draw(self):
        """
        It draws ball.
        """
        if self.owner:
            self.color = color.green
        else:
            self.color = color.yellow
        pygame.draw.ellipse(game.screen, self.color,
                            (self.x, self.y, self.r, self.r))
