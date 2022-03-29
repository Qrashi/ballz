"""
The main simulation package
"""

import pygame

import sim.objects
from .scene import Scene, Coordinate
from . import loop, window, font, constants, mouse, data, static_scene, export


scene: Scene
running = True
simulate = False
VERSION = "a0.1"

def init():
    """
    Initialize the simulation
    :return:
    """
    window.init()
    static_scene.init()
    print("O Initializing simulation", end="")
    sim.objects.ElasticBand(scene, 300, 200, sim.scene.middle(), 42.2, 3, "elastic ball 1")
    print("\r\033[K\r✓ Simulation initialized!")
    loop.screen()
    loop.start()
    pygame.quit()
    print("✓ Simulation finished!")
