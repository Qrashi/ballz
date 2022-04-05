"""
Basic scene utility classes
"""
from __future__ import annotations

import math
from typing import List, Tuple, Dict, Union

import pygame

import sim


class SceneObject:
    """A drawable object on a scene"""

    _scene: Scene

    def __init__(self, scene: Scene):
        """
        Create a new drawable object and register it in the scene
        :param scene: Scene to register to
        """
        scene.add(self)
        self._scene = scene

    def physics_tick(self, delta_t: float):
        """
        Executed every physics tick
        :param delta_t: time difference for this physics tick (seconds)
        :return:
        """

    def draw(self):
        """
        Draws the object onto a given scene
        :return:
        """

    def log(self):
        """
        Log data to the data storage
        :return:
        """

    def click(self):
        """
        Will be executed on mouse down
        :return:
        """

    def release(self):
        """
        Will be executed upon mouse up (mouse click release)
        :return:
        """


class DataObject:
    """
    A data object that holds data for a scene object or the "subparts" of a sceneobjects
    """

    name: str
    data: Dict[str, Dict[str, Union[bool, List[float]]]]

    def __init__(self, name: str, data: Dict[str, List[float]]):
        """
        Initialize the data object
        :param name: Name of the dataobject
        :param data: Initial data structure
        """
        self.data = data
        self.name = name


class Scene:
    """
    A Scene with its objects
    """

    __display: pygame.Surface
    __objects: List[SceneObject] = []
    corner: Coordinate
    data: List[DataObject] = []
    height: int
    width: int

    def __init__(self, display: pygame.Surface, corner: Coordinate, width: int, height: int):
        """
        Create a new scene
        :param display: display to draw objects to
        """
        self.__display: pygame.Surface = display
        self.height = height
        self.width = width
        self.corner = corner

    def middle(self) -> Coordinate:
        """
        Get the middle of the scene
        :return:
        """
        return Coordinate(self.width / 2, self.height / 2)

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

    def line(self, source: Coordinate, destination: Coordinate, color: Color):
        """
        Draw a line on the screen
        :param source: Where to draw from
        :param destination: Where to draw to
        :param color: Color of line
        :return:
        """
        pygame.draw.line(self.__display, color.tuple(), (self.corner + source).true_coordinates(),
                         (self.corner + destination).true_coordinates())

    def circle(self, location: Coordinate, radius: float, color: Color):
        """
        Draw a circle on the screen
        :param location: Where to draw
        :param radius: Radius of circle
        :param color: Color of circle
        :return:
        """
        pygame.draw.circle(self.__display, color.tuple(), (self.corner + location).true_coordinates(), radius)

    def text(self, location: Coordinate, text: str, color: Color, background: Color = None):
        """
        Draw a text on the screem
        :param color: Color of text
        :param text: Text to write
        :param location: Where to draw
        :param background: Background of text. None is no background
        :return:
        """
        rendered = sim.font.small_font.render(text, True, color.tuple(), background)
        rect = rendered.get_rect()
        rect.center = (self.corner + location).true_coordinates()
        self.__display.blit(rendered, rect)

    def objects(self) -> List[SceneObject]:
        """
        Return a list of all objects in the scene
        :return: A list of objects in the scene
        """
        return self.__objects

    def reset(self):
        """
        Reset the scene
        :return:
        """
        self.__objects = []
        self.data = []


class Color:
    """
    A drawable color
    """
    r: int
    g: int
    b: int
    alpha: int

    def __init__(self, r: int, g: int, b: int, alpha: int = 255):
        """
        Initialize a new color
        :param r: r value
        :param g: g value
        :param b: b value
        """
        self.alpha = alpha
        self.r: int = r
        self.g: int = g
        self.b: int = b

    def tuple(self) -> Tuple[int, int, int, int]:
        """
        Create a tuple for using colors in pygame
        :return: A tuple of all the values (r, g, b)
        """
        return self.r, self.g, self.b, self.alpha

    def __invert__(self):
        """
        Invert the color
        :return:
        """
        return Color(255 - self.r, 255 - self.g, 255 - self.b)


class Coordinate:
    """
    A coordinate on the window
    """

    x: float
    y: float

    def __init__(self, x: float, y: float):
        """
        Create a new coordinate
        :param x: x value
        :param y: y value
        """
        self.x: float = x
        self.y: float = y

    def __truediv__(self, other: float):
        """
        Divide all the components by a single number
        :param other:
        :return:
        """
        return Coordinate(self.x / other, self.y / other)

    def __mul__(self, other: float):
        """
        Multiply one vector with another scalar
        :param other:
        :return:
        """
        return Coordinate(self.x * other, self.y * other)

    def __add__(self, other: Coordinate):
        """
        Add one coordinate to another
        :param other: Other coordinate to add
        :return:
        """
        return Coordinate(self.x + other.x, self.y + other.y)

    def __sub__(self, other: Coordinate):
        """
        Subtract two coordinates
        :param other: Other coordinate to subtract
        :return:
        """
        return Coordinate(self.x - other.x, self.y - other.y)

    def __abs__(self):
        """
        Get the length of the vector
        :return:
        """
        return math.sqrt((self.x * self.x) + (self.y * self.y))

    def __str__(self) -> str:
        """
        Create a string describing the coordinate
        :return: A string describing the coordinate
        """
        return f"[x={self.x}; y={self.y}]"

    def __repr__(self):
        return "Coordinate: " + self.__str__()

    def distance(self, coordinate: Coordinate) -> float:
        """
        Get the distance between two vectors
        :param coordinate: other coordinate to measure distance to
        :return: distance
        """
        x: float = self.x - coordinate.x  # deltaY
        y: float = self.y - coordinate.y  # deltaX
        return math.sqrt(x * x + y * y)  # sqrt x^2+y^2

    def true_coordinates(self) -> Tuple[float, float]:
        """
        Create a tuple to use in pygame
        :return: A tuple of (x and y)
        """
        return self.x, sim.window.height - self.y

    def draw(self, scene: Scene, color: Color, location: Coordinate):
        """
        Draw the vector onto the scene
        :param location: Start of vector
        :param color: Color of line
        :param scene: Scene to draw to
        :return:
        """
        scene.line(location, location + self, color)
        scene.text(location + (self - location) / 2, f"l= {abs(self)}", Color(255, 255, 255))
