#!/usr/bin/env python3
""" Snake on the Next Level Game - Player File """

__author__ = 'Stephen Lee'
__email__ = 'stephenjonglee@csu.fullerton.edu'
__maintainer__ = 'stephenjonglee'

import pygame


class Player():
    """ Player class """

    def __init__(self, screen, pos, speed, color):
        """ Initialize the player """
        self._screen = screen
        self._x = pos[0]
        self._y = pos[1]
        self._length = 1
        self._size = 10
        self._body = [(self._x, self._y)]
        self._speed = speed
        self._color = color

    def get_head(self):
        """ Function gets position of the head """
        return self._x, self._y

    def get_length(self):
        """ Function gets the length of the player """
        return self._length

    def move(self, x_pos, y_pos):
        """ Function moves the player """
        x_dir = x_pos * self._speed
        y_dir = y_pos * self._speed

        self._x += x_dir
        self._y += y_dir

        self._body.append((self._x, self._y))

        # pop the body of the player.
        if len(self._body) > self._length:
            del self._body[0]

    def ate_itself(self):
        """ Returns true if the snake itself """
        head = (self._x, self._y)

        # check if head collides with body.
        for part in self._body[:-1]:
            if head == part:
                return True

        return False

    def draw(self):
        """ Draws the snake body onto the game_display """
        rad = self._size / 2
        pygame.draw.circle(self._screen, self._color,
                           (self._body[-1][0] + rad, self._body[-1][1] + rad), rad)

        for part in self._body[:-1]:
            pygame.draw.rect(self._screen, self._color, (part[0], part[1], self._size, self._size))

    def increment_length(self):
        """ Increment length """
        self._length += 1

    def get_rect(self):
        """ Return rectangle object of the snake head for collision detection """
        return pygame.Rect(self._x, self._y, self._size, self._size)
