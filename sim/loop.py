"""
The main simulation loop handler
"""
import pygame
from datetime import datetime

import sim

last_time = datetime.now()

def start():
    """
    Start the event loop
    :return:
    """
    while sim.running:
        sim.scene.draw_all()
        delta_t_diff = datetime.now() - sim.loop.last_time
        delta_t = delta_t_diff.total_seconds()
        sim.loop.last_time = datetime.now()
        if sim.simulate:
            for obj in sim.scene.objects():
                obj.physics_tick(delta_t)
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
                if event.key == pygame.K_SPACE:
                    sim.simulate = not sim.simulate
                if event.key == pygame.K_RIGHT:
                    for obj in sim.scene.objects():
                        obj.physics_tick(delta_t)
            if event.type == pygame.MOUSEBUTTONDOWN or event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    # Parse mouse click
                    for scene_object in sim.scene.objects():
                        if event.type == pygame.MOUSEBUTTONDOWN:
                            scene_object.click()
                        if event.type == pygame.MOUSEBUTTONUP:
                            scene_object.release()

