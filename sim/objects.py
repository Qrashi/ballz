"""
A file defining all simulation objects
"""
from __future__ import annotations

import math
from typing import Tuple, List

import pygame

import sim

class SceneObject:
    """A drawable object on a scene"""

    _scene: Scene

    def __init__(self, scene: Scene):
        """Create a new drawable object and register it in the scene"""
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
        pygame.draw.line(self.__display, color.tuple(), source.true_coordinates(), destination.true_coordinates())

    def circle(self, location: Coordinate, radius: float, color: Color):
        """
        Draw a circle on the screen
        :param location: Where to draw
        :param radius: Radius of circle
        :param color: Color of circle
        :return:
        """
        pygame.draw.circle(self.__display, color.tuple(), location.true_coordinates(), radius)

    def text(self, location: Coordinate, text: str, color: Color, background: Color = None):
        """
        Draw a text on the screem
        :param color: Color of text
        :param text: Text to write
        :param location: Where to draw
        :param background: Background of text. None is no background
        :return:
        """
        rendered = sim.font.main_font.render(text, True, color.tuple(), background)
        rect = rendered.get_rect()
        rect.center = location.true_coordinates()
        self.__display.blit(rendered, rect)

    def objects(self) -> List[SceneObject]:
        return self.__objects


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
        return self.x, sim.window.height-self.y

    def draw(self, scene: Scene, color: Color, location: Coordinate):
        """
        Draw the vector onto the scene
        :param location: Start of vector
        :param color: Color of line
        :param scene: Scene to draw to
        :return:
        """
        scene.line(location, location + self, color)
        scene.text(location + (self - location)/2, f"l= {abs(self)}", Color(255, 255, 255))


class Vector(Coordinate):
    """
    A physics vector
    """

    def __init__(self, x: float, y: float):
        """
        Initialize a new Vector
        :param x: x component, float
        :param y: y component, float
        """
        super().__init__(x, y)


class Ball(SceneObject):
    """
    A ball in the simulation
    """

    center: Coordinate
    size: int
    color: Color
    distance: float
    angle: float
    angular_velocity: float = 1.0
    angular_acceleration: float = 0.0
    _temp_coords: Coordinate
    __moving: bool = False

    def __init__(self, scene: Scene, angle: float, distance: float, center: Coordinate, radius: int, color: Color):
        """
        Create a new ball and register it to the scene
        :param scene: Scene to register ball to
        :param angle: Angle from center
        :param distance: distance from center
        :param center: Starting coordinates
        """
        super().__init__(scene)
        self.center = center
        self.size = radius
        self.color = color
        self.angle = angle
        self.distance = distance
        self._temp_coords = self.center + Coordinate(math.sin(self.angle) * self.distance,
                                                     math.cos(self.angle) * self.distance)

    def draw(self):
        """
        Draw a ball onto the scene
        :return:
        """
        # Calculate the "center" of the ball based on the angle and distance
        self._temp_coords = self.center + Coordinate(math.sin(self.angle) * self.distance, math.cos(self.angle) * self.distance)
        self._scene.circle(self._temp_coords, self.size, self.color)
        self._scene.text(self._temp_coords, str(round(self.angle, 2)) + "rad", Color(255, 255, 255))

    def physics_tick(self, delta_t: float):
        """
        Simulate a physics tick
        :param delta_t:
        :return:
        """

        # calculate new angular_acceleration
        self.angular_acceleration = self.angular_acceleration + delta_t * (
            self.angular_acceleration
        )

        self.angular_velocity = self.angular_velocity + self.angular_acceleration * delta_t
        self.angle = self.angle + self.angular_velocity * delta_t


class ElasticBand(SceneObject):
    """
    An elastic band that holds two balls
    """
    balls: List[Ball]
    length: float  # length from the center of one ball the center of another ball
    normal_length: float
    length_speed: float = 0.0
    length_acceleration: float = 0.0
    friction_coefficient: float
    center: Coordinate

    spring_constant: float

    def __init__(self, scene: Scene, current_length: float, normal_length: float, center: Coordinate, spring_constant: float,
                 friction_coefficient: float):
        """
        Create a new elastic band with two balls attached to it
        :param scene: Scene of elastic band
        :param current_length: Current length of band
        :param normal_length: Normal length of band (no pressure on band)
        :param spring_constant: Spring constant
        :param friction_coefficient: Friction coefficient
        """
        super().__init__(scene)
        self.balls = [
            Ball(scene, 0, current_length/2, center, 50, Color(255, 0 , 0)),
            Ball(scene, math.pi, current_length/2, center, 50, Color(0, 0, 255))
        ]
        self.normal_length = normal_length
        self.length = current_length
        self.spring_constant = spring_constant
        self.friction_coefficient = friction_coefficient
        self.center = center

        # First ball center + half of distance from one ball to another

    def physics_tick(self, delta_t: float):
        """
        Simulate one tick
        :param delta_t: delta time used
        :return:
        """
        self.length_acceleration = self.length_acceleration + delta_t * (
                2 * self.spring_constant  # 2 * spring constant
                * (abs(self.normal_length - self.length) - self.balls[0].size * 2)  # delta_l (current
                * sim.constants.G
                * self.friction_coefficient
        ) * math.copysign(1, self.length_speed)  # copy sign of "length_speed" to 1<

        self.length_speed = self.length_speed + delta_t * self.length_acceleration
        self.length = self.length + delta_t * self.length_speed

        for ball in self.balls:
            ball.distance = self.length/2

    def draw(self):
        """
        Draw the band onto the scene
        :return:
        """
        self._scene.text(self.center+Coordinate(0, 40), "l= " + str(round(self.length)), Color(255, 255, 255))
        self._scene.circle(self.center, 25, Color(0, 125, 0))
        self._scene.line(self.balls[0]._temp_coords, self.balls[1]._temp_coords, Color(255, 255, 255))

