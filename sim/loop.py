"""
The main simulation loop handler
"""
from time import perf_counter_ns
from typing import Callable

import pygame

import sim
from utils import pool

delta_t = 0.000001  # Time step to simulate
every = 5000  # How often to render a frame
realtime = 0  # Time passed since start of simulation
log_every = 1  # How often to log data (set to a higher number to use less RAM)

maxperf = "max_perf" in pool.open("config.json").json and pool.open("config.json").json["max_perf"]
disable_log = "disable_log" in pool.open("config.json").json and pool.open("config.json").json["disable_log"]
iteration: Callable[[bool], None]


def start():
    """
    Start the event loop
    :return:
    """
    while sim.running:
        # Set the last time to now, delta_t will include calculation time of the next step
        if sim.simulate:
            iteration(False)

        # Event loop
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sim.running = False
                return
            if event.type == pygame.KEYDOWN:
                # parse key presses
                if event.key == pygame.K_e:
                    sim.export.export_excel()
                if event.key == pygame.K_RIGHT:
                    sim.scenarios.next_scenario()
                if event.key == pygame.K_LEFT:
                    sim.scenarios.prev_scenario()
                if event.key == pygame.K_l:
                    sim.scenarios.reload()
                if event.key == pygame.K_DOWN:
                    iteration(True)
                if event.key == pygame.K_PAGEUP:
                    for _ in range(10):
                        iteration(False)
                    screen()
                if event.key == pygame.K_PAGEDOWN:
                    for _ in range(100):
                        iteration(False)
                    screen()
                if event.key == pygame.K_r:
                    sim.scenarios.reset()

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
                elif event.button == 3:
                    sim.data.selected = None
                screen()


def generate_tick() -> Callable[[bool], None]:
    """
    Return a function that simulates a single time step
    :return: the tick function
    """
    if maxperf:
        if disable_log:
            def tick(render: bool):
                """
                Simulate one iteration
                :param render: Force render a frame
                """
                for obj in sim.scene.objects():
                    obj.physics_tick(delta_t)
                sim.iteration += 1
                if render:
                    screen()
                    return
                if sim.iteration % every == 0:
                    screen()
        else:
            def tick(render: bool):
                """
                Simulate one iteration
                :param render: Force render a frame
                """
                for obj in sim.scene.objects():
                    obj.physics_tick(delta_t)
                    if sim.iteration % log_every == 0:
                        obj.log()
                        sim.loop.realtime += delta_t
                        sim.data.realtime.append(sim.loop.realtime)
                sim.iteration += 1
                if render:
                    screen()
                    return
                if sim.iteration % every == 0:
                    screen()
    else:
        if disable_log:
            def tick(render: bool):
                """
                Simulate one iteration
                :param render: Force render a frame
                """
                for obj in sim.scene.objects():
                    obj.physics_tick(delta_t)
                sim.iteration += 1
                if render:
                    screen()
                    return
                if sim.iteration % every == 0:
                    screen()
        else:
            def tick(render: bool):
                """
                Simulate one iteration
                :param render: Force render a frame
                """
                precalc = perf_counter_ns()
                for obj in sim.scene.objects():
                    obj.physics_tick(delta_t)
                    if sim.iteration % log_every == 0:
                        obj.log()
                        sim.data.perf_time.append(perf_counter_ns() - precalc)
                        sim.loop.realtime += delta_t
                        sim.data.realtime.append(sim.loop.realtime)
                sim.iteration += 1
                if render:
                    screen()
                    return
                if sim.iteration % every == 0:
                    screen()
    return tick


iteration = generate_tick()


def screen():
    """
    Update the screen
    :return:
    """
    sim.scene.draw_all()
    sim.data.draw()
    sim.static_scene.apply()
    pygame.display.flip()
