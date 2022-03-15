"""
The main simulation package
"""

import pygame

from sim.objects import Drawable, Scene
from . import loop, window, font

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
