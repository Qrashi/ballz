"""
The main simulation package
"""

import pygame

import sim.objects
from sim.objects import Scene
from . import loop, window

scene: Scene
running = True


def init():
    """
    Initialize the simulation
    :return:
    """
    window.init()
    print("O Initializing simulation")
    scene.add(sim.objects.Ball(scene, sim.objects.Coordinate(200, 200), 100, sim.objects.Color(255, 0, 0)))
    loop.start()
    pygame.quit()
