"""
A file defining all simulation objects
"""
from __future__ import annotations

import math
from typing import Tuple, List

import pygame

from sim.font import font


class SceneObject:
    """A drawable object on a scene"""

    _scene: Scene

    def __init__(self, scene: Scene):
        """Create a new drawable object and register it in the scene"""
        scene.add(self)
        self._scene = scene

    def draw(self):
        """
        Draws the object onto a given scene
        :return:
        """

    def click(self):
        """
        Will be executed on mouse down
        :param touches: Weather the curser touches this object
        :return:
        """

    def release(self):
        """
        Will be executed upon mouse up (mouse click release)
        :param touches: Weather the cursor touches this object
        :return:
        """


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

    def tuple(self) -> Tuple[int, int, int, int]:
        """
        Create a tuple for using colors in pygame
        :return: A tuple of all the values (r, g, b)
        """
        return self.r, self.g, self.b, 255


class Scene:
    """
    A Scene with its objects
    """

    __display: pygame.Surface
    __objects: List[SceneObject] = []

    def __init__(self, display: pygame.Surface):
        """
        Create a new scene
        :param display: display to draw objects to
        """
        self.__display: pygame.Surface = display

    def add(self, obj: SceneObject):
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
        self.__display.fill((0, 0, 0))
        for drawable in self.__objects:
            drawable.draw()
        pygame.display.update()

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
        rendered = font.render(text, True, color.tuple(), background)
        rect = rendered.get_rect()
        rect.center = (location.x, location.y)
        self.__display.blit(rendered, rect)

    def objects(self) -> List[SceneObject]:
        return self.__objects


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

    def distance(self, coordinate: Coordinate) -> float:
        """
        Get the distance between two vectors
        :param coordinate: other coordinate to measure distance to
        :return: distance
        """
        x: int = self.x - coordinate.x  # deltaY
        y: int = self.y - coordinate.y  # deltaX
        return math.sqrt(x*x + y*y)  # sqrt x^2+y^2

    def tuple(self) -> Tuple[int, int]:
        """
        Create a tuple to use in pygame
        :return: A tuple of (x and y)
        """
        return self.x, self.y


class Ball(SceneObject):
    """
    A ball in the simulation
    """

    center: Coordinate
    radius: int
    color: Color
    __moving: bool = False

    def __init__(self, scene: Scene, center: Coordinate, radius: int, color: Color):
        """
        Create a new ball and register it to the scene
        :param scene: Scene to register ball to
        :param center: Starting coordinates
        """
        super().__init__(scene)
        self.center = center
        self.radius = radius
        self.color = color

    def click(self):
        if self.center.distance(Coordinate(*pygame.mouse.get_pos())) <= self.radius:
            # If distance to mouse is less or equal distance to mouse
            self.__moving = True

    def release(self):
        if self.__moving:
            self.center = Coordinate(*pygame.mouse.get_pos())  # Unpack position tuple
            self.__moving = False

    def draw(self):
        self._scene.circle(self.center, self.radius, self.color)
        self._scene.text(self.center, str(self.radius), Color(255, 255, 255))
