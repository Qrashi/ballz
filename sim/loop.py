"""
The main simulation loop handler
"""
import pygame

import sim


def start():
    """
    Start the event loop
    :return:
    """
    while sim.running:
        sim.scene.draw_all()
        # Event loop
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sim.running = False
                return
            if event.type == pygame.KEYDOWN:
                # parse key presses
                if event.key == pygame.K_ESCAPE:
                    sim.running = False
                    return
            if event.type == pygame.MOUSEBUTTONDOWN or event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    # Parse mouse click
                    for scene_object in sim.scene.objects():
                        if event.type == pygame.MOUSEBUTTONDOWN:
                            scene_object.click()
                        if event.type == pygame.MOUSEBUTTONUP:
                            scene_object.release()

