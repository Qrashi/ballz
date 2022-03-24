import pygame.mouse

import sim


def mouse() -> sim.objects.Coordinate:
    return sim.objects.Coordinate(pygame.mouse.get_pos()[0], sim.window.height - pygame.mouse.get_pos()[1])
