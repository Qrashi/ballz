"""
Handles loading scenarios from json file and setting them up
"""
import sys

import sim

from utils import pool


scenarions = pool.open("scenarios.json")

def init():
    """
    Initialize scenarios and check for errors
    """
    if len(scenarions.json) == 0:
        print("! No scenarios defined!")
        sys.exit()
    if scenarions.json["selected"] >= len(scenarions.json["scenarios"]):
        print("! Selected scenario not defined!")
        sys.exit()
    load_current()

def load_current():
    """
    Load the current scenario
    """
    scenario = scenarions.json["scenarios"][scenarions.json["selected"]]
    sim.loop.every = scenario["simulation"]["render_every"]
    sim.loop.delta_t = scenario["simulation"]["delta_t"]
    sim.objects.ElasticBand(sim.scene,
                            scenario["setup"]["start"]["band_length"], scenario["setup"]["band"]["length"], scenario["setup"]["start"]["alpha"], sim.scene.middle(), scenario["setup"]["band"]["spring_constant"], scenario["setup"]["balls"]["friction_constant"],
                            scenario["setup"]["balls"]["mass"], scenario["setup"]["balls"]["radius"], scenario["setup"]["balls"]["torsion_constant"], scenario["setup"]["balls"]["roll_friction_constant"],
                            "scenario " + str(scenarions.json["selected"]) + " - elastic band")
    print("✓ Loaded scenario " + str(scenarions.json["selected"]))

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
    sim.data.delta_t.clear()
    print("✓ Reset")
    load_current()
    sim.loop.screen()

def next():
    """
    Switch to next scenario
    """
    if scenarions.json["selected"] + 1 < len(scenarions.json["scenarios"]):
        scenarions.json["selected"] += 1
        reset()

def prev():
    """
    Switch to previous scenario
    """
    if scenarions.json["selected"] >= 1:
        scenarions.json["selected"] -= 1
        reset()

def reload():
    """
    Reload the json file from storage and reset
    """
    prev_selected = selected()
    scenarions.reload()
    scenarions.json["selected"] = prev_selected
    reset()
    print("✓ Reloaded all scenarios")

def selected() -> int:
    """
    Get the selected scenario
    """
    return scenarions.json["selected"]
