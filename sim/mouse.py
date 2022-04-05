"""
Utilities to collect mouse data
"""
import pygame.mouse

import sim


def mouse() -> sim.scene_objects.Coordinate:
    """
    Retrieve the current mouse position
    :return: mouse position as coordinates (true coordinates)
    """
    return sim.scene_objects.Coordinate(pygame.mouse.get_pos()[0], sim.window.height - pygame.mouse.get_pos()[1])
