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
        # Set the last time to now, delta_t will include calculation time of the next step
        if sim.simulate:
            for obj in sim.scene.objects():
                obj.physics_tick(0.0333)
                obj.log()
            sim.iteration += 1
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
                if event.key == pygame.K_RIGHT:
                    for obj in sim.scene.objects():
                        obj.physics_tick(0.0333)
                        obj.log()
                    sim.iteration += 1
                    sim.data.delta_t.append(0.0333)
                    screen()
                if event.key == pygame.K_PAGEUP:
                    for i in range(10):
                        for obj in sim.scene.objects():
                            obj.physics_tick(0.0333)
                            obj.log()
                        sim.iteration += 1
                        sim.data.delta_t.append(0.0333)
                    screen()
                if event.key == pygame.K_PAGEDOWN:
                    for i in range(100):
                        for obj in sim.scene.objects():
                            obj.physics_tick(0.0333)
                            obj.log()
                        sim.iteration += 1
                        sim.data.delta_t.append(0.0333)
                    screen()
                if event.key == pygame.K_r:
                    sim.scene.reset()
                    sim.objects.ElasticBand(sim.scene,
                                            0.15, 0.15, 1, sim.scene.middle(), 1150.16, 0,
                                            0.2453, 0.02, 0.000001, 0,
                                            "elastic band 1")
                    sim.iteration = 0
                    sim.selected = None
                    print("✓ Reset")
                    screen()
                if event.key == pygame.K_ESCAPE:
                    sim.running = False
                    return
                if event.key == pygame.K_SPACE:
                    sim.simulate = not sim.simulate
            if event.type in (pygame.MOUSEBUTTONDOWN, pygame.MOUSEBUTTONUP):
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
