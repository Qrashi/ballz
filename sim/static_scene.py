"""
"Static content" to draw to every frame
"""
from typing import List, Tuple

from pygame import Surface

import sim.window

_texts: List[Tuple[Surface, Surface]] = []


def init():
    """
    Fill the texts array
    :return:
    """
    rendered = sim.font.small_font.render(
        "SPACE to simulate | ESC to quit | CLICK to select | E to export data to excel | -> next scenario | <- prev scenario | L reload scenarios from disk",
        True, (200, 200, 200), (0, 0, 0))
    rect = rendered.get_rect()
    rect.center = (rendered.get_rect().size[0] // 2, sim.window.height - rendered.get_rect().size[1] // 2)
    _texts.append((rendered, rect))


def apply():
    """
    Render all the texts onto the scene
    :return:
    """
    for text in _texts:
        sim.window.pygame_scene.blit(*text)
    rendered = sim.font.small_font.render("iteration " + str(sim.iteration), True, (81, 81, 81), (0, 0, 0))
    rect = rendered.get_rect()
    rect.center = (sim.scene.width - rendered.get_rect().size[0] // 2 - 5, rendered.get_rect().size[1] // 2)
    sim.window.pygame_scene.blit(rendered, rect)
    rendered = sim.font.small_font.render("real time: " + str(round(sim.loop.realtime, 3)) + "s", True, (255, 255, 255),
                                          (0, 0, 0))
    rect = rendered.get_rect()
    rect.center = (rendered.get_rect().size[0] // 2, rendered.get_rect().size[1] // 2)
    sim.window.pygame_scene.blit(rendered, rect)
    rendered = sim.font.small_font.render(f"scenario {sim.scenarios.selected()}; 1p = 1cm; ballz v{sim.VERSION} :)",
                                          True, (81, 81, 81), (0, 0, 0))
    rect = rendered.get_rect()
    rect.center = (
        sim.scene.width - rendered.get_rect().size[0] // 2 - 5, sim.window.height - rendered.get_rect().size[1] // 2)
    sim.window.pygame_scene.blit(rendered, rect)
