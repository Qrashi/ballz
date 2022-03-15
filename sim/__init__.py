"""
The main simulation package
"""

import pygame

from . import loop, window, font
from sim.objects import Drawable, Scene

scene: Scene
running = True


def init():
    """
    Initialize the simulation
    :return:
    """
    window.init()
    print("O Initializing simulation")

    loop.start()
    pygame.quit()
