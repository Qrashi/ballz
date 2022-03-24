"""
The main simulation package
"""

import pygame

import sim.objects
from sim.objects import Scene
from . import loop, window, font, constants, mouse


scene: Scene
running = True
simulate = False


def init():
    """
    Initialize the simulation
    :return:
    """
    window.init()
    print("O Initializing simulation")
    sim.objects.ElasticBand(scene, 600, 200, sim.window.middle, 42.2, 3)

    loop.start()
    pygame.quit()
