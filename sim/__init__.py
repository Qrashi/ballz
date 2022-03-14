import pygame

from .window import init as init_window
from .font import init as init_font

from typing import List

from sim.objects import Drawable, Scene

objects: List[Drawable] = []
scene: Scene = None

def init():
    init_window()
    init_font()
    print("O Initializing simulation")

    running = True

    while running:
        # Event loop
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                return
            elif event.type == pygame.KEYDOWN:
                # parse key presses
                if event.key == pygame.K_ESCAPE:
                    running = False

    pygame.quit()


def draw_all():
    for object in objects:
        object.draw()
