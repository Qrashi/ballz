from typing import List

import pygame

from sim.objects import Drawable, Scene
from . import loop, window, font

objects: List[Drawable] = []
scene: Scene = None
running = True


def init():
    window.init()
    font.init()
    print("O Initializing simulation")

    loop.start()
    pygame.quit()


def draw_all():
    for drawable in objects:
        drawable.draw()
