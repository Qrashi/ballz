"""
A file defining all simulation objects
"""
from __future__ import annotations

from math import copysign, cos, sin

import sim
from sim.scene_objects import SceneObject, Color, Coordinate, DataObject


class ElasticBand(SceneObject):
    """
    An elastic band that holds two balls
    """
    length: float  # length from the center of one ball the center of the rotation
    normal_length: float
    friction_coefficient: float
    spring_constant: float
    center: Coordinate

    velocity_of_ball: float = 0.0
    acceleration_of_ball: float = 0.0
    ball_radius: float
    angle_theta: float
    angular_velocity_theta: float = 0.0
    angular_acceleration_theta: float = 0.0
    ball_mass: float
    ball_moment_of_inertia: float
    ball_torsion_constant: float
    ball_rolling_friction_constant: float

    band_data: DataObject
    ball_data_1: DataObject
    ball_data_2: DataObject

    _ball_coords: Coordinate
    _ball_coords_opposite: Coordinate

    def __init__(self, scene: sim.scene_objects.Scene,
                 current_length: float, normal_length: float, delta: float, center: Coordinate, spring_constant: float,
                 friction_coefficient: float,
                 ball_mass: float, ball_radius: float, ball_torsion_constant: float, ball_roll_friction_constant: float,
                 name: str):
        """
        Create a new elastic band with two balls attached to it
        :param scene: Scene of elastic band
        :param current_length: [m] Current length of band
        :param normal_length: [m] Normal length of band (no pressure on band)
        :param spring_constant: Spring constant
        :param friction_coefficient: Friction coefficient
        :param ball_mass: [kg] mass of a ball
        :param ball_radius: [m] size of a ball
        :param delta: [rad] angle on x-axis between two balls
        :param ball_torsion_constant: Torsion constant of a ball
        :param ball_roll_friction_constant: Rolling friction constant of a ball
        """
        super().__init__(scene)
        self.normal_length = normal_length
        self.length = current_length
        self.spring_constant = spring_constant
        self.center = center

        self.friction_coefficient = friction_coefficient
        self.ball_mass = ball_mass
        self.ball_radius = ball_radius
        self.ball_torsion_constant = ball_torsion_constant
        self.ball_roll_friction_constant = ball_roll_friction_constant
        self.ball_moment_of_inertia = (2 / 5) * ball_mass * ball_radius ** 2
        self.angle_theta = (ball_radius * delta) / current_length
        self._update_coords()

        self.band_data = DataObject(name, {"length [m]": {"data": [], "export": True},
                                           "ball velocity [m/s]": {"data": [], "export": True},
                                           "ball acceleration [m/s²]": {"data": [], "export": True}})
        self.ball_data_1 = DataObject("ball 1", {"angle [rad]": {"data": [], "export": True},
                                                 "angular velocity [rad/s]": {"data": [], "export": True},
                                                 "angular acceleration [rad/s²]": {"data": [], "export": True},
                                                 "x [m]": {"data": [], "export": False},
                                                 "y [m]": {"data": [], "export": False}})
        self.ball_data_2 = DataObject("ball 2", {"angle [rad]": {"data": [], "export": True},
                                                 "angular velocity [rad/s]": {"data": [], "export": True},
                                                 "angular acceleration [rad/s²]": {"data": [], "export": True},
                                                 "x [m]": {"data": [], "export": False},
                                                 "y [m]": {"data": [], "export": False}})
        scene.data = scene.data + [self.band_data, self.ball_data_1, self.ball_data_2]

    def _update_coords(self):
        """
        Update the temporary ball coordinates
        :return:
        """
        change = Coordinate(cos(self.angle_theta) * (self.length * 1000),
                            sin(self.angle_theta) * (self.length * 1000))

        self._ball_coords = self.center + change
        self._ball_coords_opposite = self.center - change

    def log(self):
        """
        Log the current state of the elastic band
        :return:
        """
        self.band_data.data["length [m]"]["data"].append(self.length)
        self.band_data.data["ball velocity [m/s]"]["data"].append(self.velocity_of_ball)
        self.band_data.data["ball acceleration [m/s²]"]["data"].append(self.acceleration_of_ball)
        self.ball_data_1.data["angle [rad]"]["data"].append(self.angle_theta)
        self.ball_data_1.data["angular velocity [rad/s]"]["data"].append(self.angular_velocity_theta)
        self.ball_data_1.data["angular acceleration [rad/s²]"]["data"].append(self.angular_acceleration_theta)
        self.ball_data_1.data["x [m]"]["data"].append(self._ball_coords.x)
        self.ball_data_1.data["y [m]"]["data"].append(self._ball_coords.y)
        self.ball_data_2.data["angle [rad]"]["data"].append(self.angle_theta)
        self.ball_data_2.data["angular velocity [rad/s]"]["data"].append(self.angular_velocity_theta)
        self.ball_data_2.data["angular acceleration [rad/s²]"]["data"].append(self.angular_acceleration_theta)
        self.ball_data_2.data["x [m]"]["data"].append(self._ball_coords_opposite.x)
        self.ball_data_2.data["y [m]"]["data"].append(self._ball_coords_opposite.y)

    def physics_tick(self, delta_t: float):
        """
        Simulate one tick
        :param delta_t: delta time used
        :return:
        """
        self.acceleration_of_ball = (
                                            - 1.42 * self.spring_constant  # 2 * spring constant
                                            * max(self.length - self.normal_length, 0)  # delta_l
                                            - 2 * self.ball_mass * sim.constants.g
                                            * (self.friction_coefficient * copysign(1, self.velocity_of_ball))  # - friction
                                            + (self.angular_velocity_theta ** 2) * self.ball_mass * self.length  # centrifugal force
                                    ) / self.ball_mass  # copy sign of "length_speed" to the current acceleration
        
        self.velocity_of_ball = self.velocity_of_ball + delta_t * self.acceleration_of_ball
        self.length = self.length + delta_t * self.velocity_of_ball

        self.angular_acceleration_theta = (
                                                  (-2 * self.ball_torsion_constant) * ((self.angle_theta * self.length) / self.ball_radius)
                                                  - self.ball_roll_friction_constant
                                                  * self.ball_mass * sim.constants.g
                                          ) / (2 * (self.ball_moment_of_inertia + self.ball_mass * self.length ** 2))

        self.angular_velocity_theta = self.angular_velocity_theta + self.angular_acceleration_theta * delta_t
        self.angle_theta = self.angle_theta + self.angular_velocity_theta * delta_t

    def draw(self):
        """
        Draw the band onto the scene
        :return:
        """
        self._update_coords()
        self._scene.circle(self.center, 10, Color(0, 125, 0, alpha=10))
        self._scene.line(self._ball_coords, self._ball_coords_opposite, Color(255, 255, 255))
        self._scene.circle(self._ball_coords, self.ball_radius * 1000,
                           Color(0, 255, 255))  # Conversion from m to cm (px)
        self._scene.circle(self._ball_coords_opposite, self.ball_radius * 1000, Color(255, 255, 0))

    def click(self):
        """
        Check if object was clicked and select it
        """
        if sim.mouse.mouse().distance(self.center) <= 10:
            sim.data.selected = self.band_data
            return

        if sim.mouse.mouse().distance(self._ball_coords) <= self.ball_radius * 500:
            sim.data.selected = self.ball_data_1
            return

        if sim.mouse.mouse().distance(self._ball_coords_opposite) <= self.ball_radius * 500:
            sim.data.selected = self.ball_data_2
            return
