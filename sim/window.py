"""
Window utilities
"""
import pygame

import sim
from sim.objects import Scene, Coordinate


width: int
height: int
middle: Coordinate

def init():
    """
    Initialize the pygame window
    :return:
    """
    pygame.init()
    info = pygame.display.Info()
    sim.window.width, sim.window.height = info.current_w * 0.8, info.current_h * 0.8
    window = pygame.display.set_mode((sim.window.width, sim.window.height))
    pygame.display.set_caption("ballz", "ballz simulation")
    pygame.display.set_icon(pygame.image.load("icon.png", "burning football"))
    sim.scene = Scene(window)
    sim.window.middle = Coordinate(sim.window.width/2, sim.window.height/2)
