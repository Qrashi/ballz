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
        if sim.simulate:
            delta_t_diff = datetime.now() - sim.loop.last_time
            delta_t = delta_t_diff.total_seconds()
        sim.loop.last_time = datetime.now()
        # Set the last time to now, delta_t will include calculation time of the next step
        if sim.simulate:
            for obj in sim.scene.objects():
                obj.physics_tick(delta_t)
                obj.log()
            sim.data.delta_t.append(delta_t)
            screen()

        # Event loop
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sim.running = False
                return
            if event.type == pygame.KEYDOWN:
                # parse key presses
                if event.key == pygame.K_e:
                    sim.export.export_excel()
                    print("✓ Exported to excel")
                if event.key == pygame.K_ESCAPE:
                    sim.running = False
                    return
                if event.key == pygame.K_SPACE:
                    sim.simulate = not sim.simulate
            if event.type == pygame.MOUSEBUTTONDOWN or event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    # Parse mouse click
                    for scene_object in sim.scene.objects():
                        if event.type == pygame.MOUSEBUTTONDOWN:
                            scene_object.click()
                        if event.type == pygame.MOUSEBUTTONUP:
                            scene_object.release()
                    screen()


def screen():
    """
    Update the screen
    :return:
    """
    sim.scene.draw_all()
    sim.data.draw()
    sim.static_scene.apply()
    pygame.display.flip()

