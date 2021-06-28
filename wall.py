import pygame


class Wall(object):
    """ Wall class """

    def __init__(self, screen, x, y, width, height, color):
        """ Initialize block is position and size """
        self._x = x
        self._y = y
        self._width = width
        self._height = height
        self._screen = screen
        self._color = color

    def draw(self):
        """ Function draws the wall on screen """
        pygame.draw.rect(self._screen, self._color, (self._x, self._y, self._width, self._height))

    def get_pos(self):
        """ Function gets the position of the wall """
        return (self._x, self._y)

    def get_rect(self):
        """ Function gets the rectangle object of the wall """
        return pygame.Rect(self._x, self._y, self._width, self._height)
