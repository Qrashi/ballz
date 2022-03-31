"""
The main simulation package
"""

import pygame
import math

from datetime import datetime

import sim.objects
from .scene import Scene, Coordinate
from . import loop, window, font, constants, mouse, data, static_scene, export


scene: Scene
iteration: int = 0
running = True
simulate = False
VERSION = "a0.1"
start = datetime.now().timestamp()


def init():
    """
    Initialize the simulation
    :return:
    """
    window.init()
    font.init()
    static_scene.init()
    print("O Initializing simulation", end="")
    sim.objects.ElasticBand(scene,
                            0.15, 0.15, math.pi, sim.scene.middle(), 1150.16, 0.1,
                            0.2453, 0.02, 0.000001, 0,
                            "elastic band 1")
    print("\r\033[K\r✓ Simulation initialized!")
    loop.screen()
    loop.start()
    pygame.quit()
    print("✓ Simulation finished!")
