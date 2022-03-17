"""
Window utilities
"""
import pygame

import sim
from sim.objects import Scene


def init():
    """
    Initialize the pygame window
    :return:
    """
    pygame.init()
    info = pygame.display.Info()
    window = pygame.display.set_mode((info.current_w * 0.8, info.current_h * 0.8))
    pygame.display.set_caption("ballz simulation", "simulation")
    pygame.display.set_icon(pygame.image.load("icon.png", "burning football"))
    sim.scene = Scene(window)
