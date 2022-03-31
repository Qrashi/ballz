"""
The main simulation package
"""

import pygame

from datetime import datetime

import sim.objects
from .scene import Scene, Coordinate
from . import loop, window, font, constants, mouse, data, static_scene, export


scene: Scene
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
                            0.2, 0.15, sim.scene.middle(), 42.42, 3.5, 0.001,
                            0.02, 0.03, 1.2, -1.6,
                            "elastic band 1")
    print("\r\033[K\r✓ Simulation initialized!")
    loop.screen()
    loop.start()
    pygame.quit()
    print("✓ Simulation finished!")
