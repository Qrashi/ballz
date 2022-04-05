"""
The main simulation package
"""

from datetime import datetime

import pygame

import sim.objects
from . import loop, window, font, constants, mouse, data, static_scene, export, scenarios
from .scene import Scene, Coordinate

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
    print("\r\033[K\rOK Simulation initialized!")
    loop.screen()
    loop.start()
    pygame.quit()
    print("OK Simulation finished!")
