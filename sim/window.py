"""
Window utilities
"""
import math

import pygame

import sim
from sim.scene_objects import Coordinate

width: int
height: int
middle: Coordinate
pygame_scene: pygame.display


def init():
    """
    Initialize the pygame window
    :return:
    """
    pygame.init()
    info = pygame.display.Info()
    pygame.display.set_caption(f"ballz v{sim.VERSION}", "ballz simulation")
    sim.window.width, sim.window.height = int(math.floor(info.current_w * 0.8)), int(math.floor(info.current_h * 0.8))
    sim.window.pygame_scene = pygame.display.set_mode((sim.window.width, sim.window.height))
    pygame.display.set_icon(pygame.image.load("icon.png", "burning football"))
    scene_x = math.floor(sim.window.width * 0.8)
    sim.scene = sim.scene_objects.Scene(pygame_scene, Coordinate(0, 0), scene_x, sim.window.height)
    sim.data.corner = Coordinate(scene_x, 0)
    sim.window.middle = Coordinate(sim.window.width / 2, sim.window.height / 2)
