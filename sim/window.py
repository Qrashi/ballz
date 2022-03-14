import pygame

from .objects import Scene


def init():
    pygame.init()
    info = pygame.display.Info()
    window = pygame.display.set_mode((info.current_w * 0.8, info.current_h * 0.8))
    scene = Scene(window)
