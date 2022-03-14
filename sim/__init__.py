import pygame

from .window import init as init_window
from .font import init as init_font
import sim.loop

from typing import List

from sim.objects import Drawable, Scene

objects: List[Drawable] = []
scene: Scene = None
running = True

def init():
    init_window()
    init_font()
    print("O Initializing simulation")

    loop.start()
    pygame.quit()


def draw_all():
    for object in objects:
        object.draw()
