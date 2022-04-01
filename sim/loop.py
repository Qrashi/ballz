"""
The main simulation loop handler
"""
import pygame
from time import perf_counter_ns

import sim

delta_t = 0.000001  # Time step to simulate
every = 5000  # How often to render a frame
realtime = 0  # Time passed since start of simulation

def start():
    """
    Start the event loop
    :return:
    """
    while sim.running:
        # Set the last time to now, delta_t will include calculation time of the next step
        if sim.simulate:
            tick(False)

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
                    sim.scenarios.next()
                if event.key == pygame.K_LEFT:
                    sim.scenarios.prev()
                if event.key == pygame.K_l:
                    sim.scenarios.reload()
                if event.key == pygame.K_DOWN:
                    tick(True)
                if event.key == pygame.K_PAGEUP:
                    for _ in range(10):
                        tick(False)
                    screen()
                if event.key == pygame.K_PAGEDOWN:
                    for _ in range(100):
                        tick(False)
                    screen()
                if event.key == pygame.K_r:
                    sim.scenarios.reset()
                
                if event.key == pygame.K_ESCAPE:
                    sim.running = False
                    return
                if event.key == pygame.K_SPACE:
                    sim.simulate = not sim.simulate
            if event.type in (pygame.MOUSEBUTTONDOWN, pygame.MOUSEBUTTONUP) and event.button == 1:
                # Parse mouse click
                for scene_object in sim.scene.objects():
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        scene_object.click()
                    if event.type == pygame.MOUSEBUTTONUP:
                        scene_object.release()
                screen()


def tick(render: bool):
    """
    Simulate one iteration
    :param render: Force render a frame
    """
    precalc = perf_counter_ns()
    for obj in sim.scene.objects():
        obj.physics_tick(delta_t)
        obj.log()
    sim.iteration += 1
    sim.data.delta_t.append(perf_counter_ns() - precalc)
    sim.loop.realtime += delta_t
    sim.data.realtime.append(sim.loop.realtime)
    if render:
        screen()
        return
    if sim.iteration % every == 0:
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
