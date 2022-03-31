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
    size: float
    color: Color
    distance: float
    angle: float
    angular_velocity: float = 0.0
    angular_acceleration: float = 0.0
    mass: float
    moment_of_inertia: float
    torsion_constant: float
    some_constant: float
    _temp_coords: Coordinate

    def __init__(self, scene: sim.Scene, angle: float, distance: float, center: Coordinate, radius: float, color: Color,
                 mass: float, torsion_constant: float, some_constant: float, name: str):
        """
        Create a new ball and register it to the scene
        :param scene: Scene to register ball to
        :param angle: [rad] Angle from center
        :param distance: [m] distance from center
        :param center: Middle coordinates
        :param radius: [m] radius
        :param mass: [kg] mass of ball
        """
        super().__init__(scene, {"x [p|cm]": [], "y [p|cm]": [], "angle [rad]": [], "angular velocity [rad/s]": [], "angular acceleration [rad/s²]": []}, name)
        self.center = center
        self.size = radius
        self.color = color
        self.mass = mass
        self.angle = angle
        self.distance = distance
        self.torsion_constant = torsion_constant
        self.some_constant = some_constant
        self.moment_of_inertia = (2 / 5) * self.mass * radius * radius
        self._temp_coords = self.center + Coordinate(math.sin(self.angle) * (self.distance * 1000),
                                                     math.cos(self.angle) * (self.distance * 1000))

    def draw(self):
        """
        Draw a ball onto the scene
        :return:
        """
        # Calculate the "center" of the ball based on the angle and distance
        # self.distance * 1000 (conversion from m to cm)
        try:
            self._temp_coords = self.center + Coordinate(math.sin(self.angle) * (self.distance * 1000),
                                                         math.cos(self.angle) * (self.distance * 1000))
        except ValueError:
            print("! Error: could not calculate sinus or cosinus of angle")
            print(f"! Current angle {self.angle}rad")
            sim.export.export_excel()
            print("✓ Exported data to excel")
            sim.simulate = False
        self._scene.circle(self._temp_coords, (self.size * 1000), self.color)
        self._scene.text(self._temp_coords + Coordinate(0, (self.size * 1000) + 20), str(round(self.angle, 2)),
                         Color(255, 255, 255))

    def log(self):
        """
        Log data to data storage
        :return:
        """
        self.data["x [p|cm]"].append(self._temp_coords.x)
        self.data["y [p|cm]"].append(self._temp_coords.y)
        self.data["angle [rad]"].append(self.angle)
        self.data["angular velocity [rad/s]"].append(self.angular_velocity)
        self.data["angular acceleration [rad/s²]"].append(self.angular_acceleration)

    def click(self):
        """
        Handle a click on the ball and select if clicked
        """
        if sim.mouse.mouse().distance(self._temp_coords) <= self.size:
            sim.data.selected = self

    def physics_tick(self, delta_t: float):
        """
        Simulate a physics tick
        :param delta_t:
        :return:
        """
        self.angular_acceleration = self.angular_acceleration + delta_t * (
            -2 * (self.torsion_constant * self.size)
            * self.angle
            * self.distance
            - self.some_constant
            * (self.angular_velocity * self.distance + self.angular_velocity * self.angle) / self.size
        ) / self.moment_of_inertia

        self.angular_velocity = self.angular_velocity + self.angular_acceleration * delta_t
        self.angle = self.angle + self.angular_velocity * delta_t

    @property
    def temp_coords(self):
        return self._temp_coords


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
    mass: float

    spring_constant: float

    def __init__(self, scene: sim.Scene,
                 current_length: float, normal_length: float, center: Coordinate, spring_constant: float, friction_coefficient: float, mass: float,
                 ball_mass: float, ball_radius: float, ball_torsion_constant: float, ball_some_constant: float,
                 name: str):
        """
        Create a new elastic band with two balls attached to it
        :param scene: Scene of elastic band
        :param current_length: [m] Current length of band
        :param normal_length: [m] Normal length of band (no pressure on band)
        :param spring_constant: Spring constant
        :param friction_coefficient: Friction coefficient
        :param mass: [kg] mass
        :param ball_mass: [kg] mass of a ball
        :param ball_radius: [m] size of a ball
        """
        super().__init__(scene, {"length [p|cm]": [], "length speed [cm/s]": [], "length acceleration [cm/s²]": []}, name)
        self.balls = [
            Ball(scene,
                 0, current_length / 2, center, ball_radius, Color(255, 0, 0), ball_mass, ball_torsion_constant, ball_some_constant,
                 name + " | ball 1"),
            Ball(scene,
                 math.pi, current_length / 2, center, ball_radius, Color(0, 0, 255), ball_mass, ball_torsion_constant, ball_some_constant,
                 name + " | ball 2")
        ]
        self.normal_length = normal_length
        self.length = current_length
        self.spring_constant = spring_constant
        self.friction_coefficient = friction_coefficient
        self.center = center
        self.mass = mass

        # First ball center + half of distance from one ball to another

    def physics_tick(self, delta_t: float):
        """
        Simulate one tick
        :param delta_t: delta time used
        :return:
        """
        self.length_acceleration = self.length_acceleration + delta_t * math.copysign(
            2 * self.spring_constant  # 2 * spring constant
            * (abs(self.length - self.normal_length) - self.balls[0].size * 2)  # delta_l (current
            * sim.constants.G
            * self.friction_coefficient
            , self.length_speed) / self.mass  # copy sign of "length_speed" to the current acceleration

        self.length_speed = self.length_speed + delta_t * self.length_acceleration
        self.length = self.length + delta_t * self.length_speed

        for ball in self.balls:
            ball.distance = self.length / 2

    def draw(self):
        """
        Draw the band onto the scene
        :return:
        """
        self._scene.text(self.center + Coordinate(0, 40), "l= " + str(round(self.length * 1000)), Color(255, 255, 255))
        self._scene.circle(self.center, 25, Color(0, 125, 0))
        self._scene.line(self.balls[0].temp_coords, self.balls[1].temp_coords, Color(255, 255, 255))

    def click(self):
        """
        Check if object was clicked and select it
        """
        if sim.mouse.mouse().distance(self.center) <= 25:
            sim.data.selected = self

    def log(self):
        """
        Log data to data storage
        """
        self.data["length [p|cm]"].append(self.length)
        self.data["length speed [cm/s]"].append(self.length_speed)
        self.data["length acceleration [cm/s²]"].append(self.length_acceleration)
