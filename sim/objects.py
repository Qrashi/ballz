from __future__ import annotations

from typing import Tuple

import pygame

from sim import objects


class Drawable:
    def __init__(self):
        objects.append(self)

    def draw(self):
        pass


class Color:
    """
    A drawable color
    """

    def __init__(self, r: int, g: int, b: int):
        self.r: int = r
        self.g: int = g
        self.b: int = b

    def tuple(self) -> Tuple[int, int, int]:
        return self.r, self.g, self.b


class Scene:
    """
    Defines helper functions for a pygame display
    """

    def __init__(self, display: pygame.display):
        self.display: pygame.display = display

    def line(self, source: Coordinate, destination: Coordinate, color: Color):
        """
        Draw a line on the screen
        :param source: Where to draw from
        :param destination: Where to draw to
        :param color: Color of line
        :return:
        """
        pygame.draw.line(self.display, color.tuple(), source.tuple(), destination.tuple())

    def circle(self, location: Coordinate, radius: float, color: Color):
        """
        Draw a circle on the screen
        :param location: Where to draw
        :param radius: Radius of circle
        :param color: Color of circle
        :return:
        """
        pygame.draw.circle(self.display, color.tuple(), location.tuple(), radius)

    def text(self, location: Coordinate):
        pass


class Coordinate:
    """
    A coordinate on the window
    """

    def __init__(self, x: int, y: int):
        self.x: int = x
        self.y: int = y

    def __add__(self, other: Coordinate):
        self.x = self.x + other.x
        self.y = self.y + other.y

    def __sub__(self, other: Coordinate):
        self.x = self.x - other.x
        self.y = self.y - other.y

    def __str__(self) -> str:
        return f"[x{self.x}; y{self.y}]"

    def tuple(self) -> Tuple[int, int]:
        return self.x, self.y


class Ball(Drawable):
    """
    Defines a ball in the simulation
    """

    def __init__(self, center: Coordinate):
        super().__init__()
        self.center: Coordinate = center

    def draw(self):
        pass
