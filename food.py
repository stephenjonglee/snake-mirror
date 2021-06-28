#!/usr/bin/env python3
""" Snake on the Next Level Game - Food File """

__author__ = 'Stephen Lee'
__email__ = 'stephenjonglee@csu.fullerton.edu'
__maintainer__ = 'stephenjonglee'

import random
import pygame

class Food():
    """ Food class """

    def __init__(self, screen, pos, color, size=10):
        """ Initialize food """
        self._screen = screen
        self._x = pos[0]
        self._y = pos[1]
        self._size = size
        self._color = color

    def generate_food(self):
        """ Function generate random location """
        (width, height) = self._screen.get_size()
        cell_size = 10
        wall_size = 10
        buffer = 40
        self._x = round(random.randrange(0 + wall_size + buffer, width - wall_size, cell_size))
        self._y = round(random.randrange(0 + wall_size + buffer, height - wall_size, cell_size))

        return (self._x, self._y)

    def draw(self):
        """ Function draws the food """
        pygame.draw.rect(self._screen, self._color, (self._x, self._y, self._size, self._size))

    def get_pos(self):
        """ Function returns the position of food """
        return (self._x, self._y)

    def get_rect(self):
        """ Function return rectangle object of food """
        return pygame.Rect(self._x, self._y, self._size, self._size)
