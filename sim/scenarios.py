"""
Handles loading scenarios from json file and setting them up
"""
import sys

import sim
from utils import pool

scenarios = pool.open("scenarios.json")


def init():
    """
    Initialize scenarios and check for errors
    """
    if len(scenarios.json) == 0:
        print("! No scenarios defined!")
        sys.exit()
    if scenarios.json["selected"] >= len(scenarios.json["scenarios"]):
        print("! Selected scenario not defined!")
        sys.exit()
    load_current()


def load_current():
    """
    Load the current scenario
    """
    scenario = scenarios.json["scenarios"][scenarios.json["selected"]]
    sim.loop.every = scenario["simulation"]["render_every"]
    sim.loop.delta_t = scenario["simulation"]["delta_t"]
    sim.loop.log_every = scenario["simulation"]["log_every"]
    sim.loop.iteration = sim.loop.generate_tick()
    sim.objects.ElasticBand(sim.scene,
                            scenario["setup"]["start"]["band_length"], scenario["setup"]["band"]["length"],
                            scenario["setup"]["start"]["alpha"], sim.scene.middle(),
                            scenario["setup"]["band"]["spring_constant"],
                            scenario["setup"]["balls"]["friction_constant"],
                            scenario["setup"]["balls"]["mass"], scenario["setup"]["balls"]["radius"],
                            scenario["setup"]["balls"]["torsion_constant"],
                            scenario["setup"]["balls"]["roll_friction_constant"],
                            "elastic band")
    print("OK Loaded scenario " + str(scenarios.json["selected"]))


def reset():
    """
    Reset current scenario
    """
    sim.scene.reset()
    sim.iteration = 0
    sim.simulate = False
    sim.data.selected = None
    sim.data.realtime = []
    sim.loop.realtime = 0
    sim.data.perf_time.clear()
    print("OK Reset")
    load_current()
    sim.loop.screen()


def next_scenario():
    """
    Switch to next scenario
    """
    if scenarios.json["selected"] + 1 < len(scenarios.json["scenarios"]):
        scenarios.json["selected"] += 1
        reset()


def prev_scenario():
    """
    Switch to previous scenario
    """
    if scenarios.json["selected"] >= 1:
        scenarios.json["selected"] -= 1
        reset()


def reload():
    """
    Reload the json file from storage and reset
    """
    prev_selected = selected()
    scenarios.reload()
    scenarios.json["selected"] = prev_selected
    reset()
    print("OK Reloaded all scenarios")


def selected() -> int:
    """
    Get the selected scenario
    """
    return scenarios.json["selected"]
