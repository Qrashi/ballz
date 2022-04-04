"""
The main simulation package
"""

import pygame
import math

from datetime import datetime

import sim.objects
from .scene import Scene, Coordinate
from . import loop, window, font, constants, mouse, data, static_scene, export, scenarios


scene: Scene
iteration: int = 0
running = True
simulate = False
VERSION = "a0.2"
start = datetime.now().timestamp()


def init():
    """
    Initialize the simulation
    :return:
    """
    window.init()
    font.init()
    static_scene.init()
    scenarios.init()
    # sim.objects.ElasticBand(scene,
    #                         0.2, 0.17, 2*math.pi, sim.scene.middle(), 1150.16, 0.1,
    #                         0.2453, 0.02, 0.001897, 0.1,
    #                         "elastic band 1")
    print("\r\033[K\rOK Simulation initialized!")
    loop.screen()
    loop.start()
    pygame.quit()
    print("OK Simulation finished!")
