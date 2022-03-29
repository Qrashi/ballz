import pygame.mouse

import sim
import sim.scene


def mouse() -> sim.Coordinate:
    return sim.Coordinate(pygame.mouse.get_pos()[0], sim.window.height - pygame.mouse.get_pos()[1])
