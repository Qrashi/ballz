"""
A file defining all simulation objects
"""
from __future__ import annotations

from typing import Tuple, List

from sim.font import font

import pygame


class Drawable:
    """
    A general type
    """
    __scene: Scene

    def __init__(self, scene: Scene):
        """
        Create a new drawable object and register it in the scene
        """
        scene.add(self)
        self.__scene = scene

    def draw(self):
        """
        Draws the object onto a given scene
        :return:
        """
        ...


class Color:
    """
    A drawable color
    """

    def __init__(self, r: int, g: int, b: int):
        """
        Initialize a new color
        :param r: r value
        :param g: g value
        :param b: b value
        """
        self.r: int = r
        self.g: int = g
        self.b: int = b

    def tuple(self) -> Tuple[int, int, int]:
        """
        Create a tuple for using colors in pygame
        :return: A tuple of all the values (r, g, b)
        """
        return self.r, self.g, self.b


class Scene:
    """
    A Scene with its objects
    """

    __display: pygame.Surface
    __objects: List[Drawable] = []

    def __init__(self, display: pygame.Surface):
        """
        Create a new scene
        :param display: display to draw objects to
        """
        self.__display: pygame.Surface = display

    def add(self, obj: Drawable):
        """
        Add an object to the scene
        :param obj: Object to add (must be of type Drawable)
        :return:
        """
        self.__objects.append(obj)

    def draw_all(self):
        """
        Redraw all objects
        :return:
        """
        for drawable in self.__objects:
            drawable.draw()

    def line(self, source: Coordinate, destination: Coordinate, color: Color):
        """
        Draw a line on the screen
        :param source: Where to draw from
        :param destination: Where to draw to
        :param color: Color of line
        :return:
        """
        pygame.draw.line(self.__display, color.tuple(), source.tuple(), destination.tuple())

    def circle(self, location: Coordinate, radius: float, color: Color):
        """
        Draw a circle on the screen
        :param location: Where to draw
        :param radius: Radius of circle
        :param color: Color of circle
        :return:
        """
        pygame.draw.circle(self.__display, color.tuple(), location.tuple(), radius)

    def text(self, location: Coordinate, text: str, color: Color, background: Color = None):
        """
        Draw a text on the screem
        :param color: Color of text
        :param text: Text to write
        :param location: Where to draw
        :param background: Background of text. None is no background
        :return:
        """
        rendered = font.render(text, True, color.tuple(), background = background)
        rect = rendered.get_rect()
        rect.center = (location.x // 2, location.y // 2)
        self.__display.blit(rendered, rect)


class Coordinate:
    """
    A coordinate on the window
    """
    x: int
    y: int

    def __init__(self, x: int, y: int):
        """
        Create a new coordinate
        :param x: x value
        :param y: y value
        """
        self.x: int = x
        self.y: int = y

    def __add__(self, other: Coordinate):
        """
        Add one coordinate to another
        :param other: Other coordinate to add
        :return:
        """
        self.x = self.x + other.x
        self.y = self.y + other.y

    def __sub__(self, other: Coordinate):
        """
        Subtract two coordinates
        :param other: Other coordinate to subtract
        :return:
        """
        self.x = self.x - other.x
        self.y = self.y - other.y

    def __str__(self) -> str:
        """
        Create a string describing the coordinate
        :return: A string describing the coordinate
        """
        return f"[x{self.x}; y{self.y}]"

    def tuple(self) -> Tuple[int, int]:
        """
        Create a tuple to use in pygame
        :return: A tuple of (x and y)
        """
        return self.x, self.y