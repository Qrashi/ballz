"""
A file defining all simulation objects
"""
from __future__ import annotations

import math
from typing import List

import sim
from sim.scene import SceneObject, Color, Coordinate


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

    def __init__(self, scene: sim.Scene, angle: float, distance: float, center: Coordinate, radius: int, color: Color, name: str):
        """
        Create a new ball and register it to the scene
        :param scene: Scene to register ball to
        :param angle: Angle from center
        :param distance: distance from center
        :param center: Starting coordinates
        """
        super().__init__(scene, {"x [p]": [], "y [p]": [], "angle [rad]": []}, name)
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
        self._scene.text(self._temp_coords + Coordinate(0, self.size + 20), str(round(self.angle, 2)), Color(255, 255, 255))

    def log(self):
        """
        Log data to data storage
        :return:
        """
        self.data["x [p]"].append(self._temp_coords.x)
        self.data["y [p]"].append(self._temp_coords.y)
        self.data["angle [rad]"].append(self.angle)

    def click(self):
        if sim.mouse.mouse().distance(self._temp_coords) <= self.size:
            sim.data.select(self)

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

    def __init__(self, scene: sim.Scene, current_length: float, normal_length: float, center: Coordinate, spring_constant: float,
                 friction_coefficient: float, name: str):
        """
        Create a new elastic band with two balls attached to it
        :param scene: Scene of elastic band
        :param current_length: Current length of band
        :param normal_length: Normal length of band (no pressure on band)
        :param spring_constant: Spring constant
        :param friction_coefficient: Friction coefficient
        """
        super().__init__(scene, {"length [p]": [], "length speed [p/s]": [], "length acceleration [p/s²]": []}, name)
        self.balls = [
            Ball(scene, 0, current_length / 2, center, 50, Color(255, 0, 0), name + " | ball 1"),
            Ball(scene, math.pi, current_length / 2, center, 50, Color(0, 0, 255), name + " | ball 2")
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
        # self.length_acceleration = self.length_acceleration + delta_t * math.copysign(
        #         2 * self.spring_constant  # 2 * spring constant
        #         * (abs(self.normal_length - self.length) - self.balls[0].size * 2)  # delta_l (current
        #         * sim.constants.G
        #         * self.friction_coefficient
        # , self.length_speed)  # copy sign of "length_speed" to the current acceleration

        self.length_acceleration = self.length_acceleration + delta_t * math.sin(self.length - self.normal_length)

        # print(f"delta t: {delta_t}s")
        # print(f"delta l: {abs(self.normal_length - self.length) - self.balls[0].size * 2}u")
        # print(f"length acceleration: {self.length_acceleration}")

        self.length_speed = self.length_speed + delta_t * self.length_acceleration
        self.length = self.length + delta_t * self.length_speed

        for ball in self.balls:
            ball.distance = self.length/2

    def draw(self):
        """
        Draw the band onto the scene
        :return:
        """
        self._scene.text(self.center + Coordinate(0, 40), "l= " + str(round(self.length)), Color(255, 255, 255))
        self._scene.circle(self.center, 25, Color(0, 125, 0))
        self._scene.line(self.balls[0]._temp_coords, self.balls[1]._temp_coords, Color(255, 255, 255))

    def click(self):
        if sim.mouse.mouse().distance(self.center) <= 25:
            sim.data.select(self)

    def log(self):
        self.data["length [p]"].append(self.length)
        self.data["length speed [p/s]"].append(self.length_speed)
        self.data["length acceleration [p/s²]"].append(self.length_acceleration)

