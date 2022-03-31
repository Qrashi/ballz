from typing import List, Dict, Tuple

import pygame

import sim.window
from sim.scene import Coordinate, SceneObject, Color

corner: Coordinate
selected: SceneObject = None

delta_t: List[int] = []
_font_cache: Dict[str, pygame.Surface] = {}


def draw():
    """
    Draw the plots onto the screen
    :return:
    """
    # Draw the basic "box" for data
    if selected is None:
        # No data
        pygame.draw.line(sim.window.pygame_scene, (255, 255, 255), (corner.x, corner.y), (corner.x, sim.window.height),
                         width=10)
        rendered = sim.font.main_font.render("object inspector", True, (255, 255, 255), (0, 0, 0))
        obj_rect = rendered.get_rect()
        obj_rect.center = (corner.x + (sim.window.width - corner.x) // 2, corner.y + (sim.window.height - corner.y) // 2)
        sim.window.pygame_scene.blit(rendered, obj_rect)
        rendered = sim.font.main_font.render("click to select", True, (255, 255, 255), (0, 0, 0))
        rect = rendered.get_rect()
        rect.center = (corner.x + (sim.window.width - corner.x) // 2,
                       corner.y + (sim.window.height - corner.y) // 2 + obj_rect.size[1] * 2)
        sim.window.pygame_scene.blit(rendered, rect)
        return
    plots = min(len(selected.data), 6)  # Max plots to display is 6
    plot_y_size = sim.window.height // plots
    # The number of plots to display, if the number of plots in the selected sceneobjects are more than the window can fit (height / plot y size)
    current_plot = 0
    data_incl_perf = selected.data.copy()
    data_incl_perf["delta t [s]"] = delta_t
    for plot_name, data in data_incl_perf.items():
        if len(data) == 0:
            value_rendered = _font("no data", (100, 100, 100))
        else:
            value_rendered = sim.font.small_font.render(str(round(data[len(data) - 1], 5)), True, (100, 100, 100),
                                                        (0, 0, 0))
        rendered = _font(plot_name, (255, 255, 255))
        value_rect = value_rendered.get_rect()
        rect = rendered.get_rect()
        # size = (x_size, y_size)
        # max x - rect x size / 2, current plot * plot y size + rect y size / 2
        value_rect.center = (sim.window.width - value_rect.size[0] // 2, (current_plot + 1) * plot_y_size + rect.size[1] // 2 - 40)
        # plot_y_size down and 10 up because bottom edge of graph
        rect.center = (sim.window.width - rect.size[0] // 2 - 5, current_plot * plot_y_size + rect.size[1] // 2 + 10)
        # +10 for white line width
        # data * scale = y pos
        # delta is the maximum change to 0
        if len(data) == 0:
            delta = 1
        else:
            delta = max(abs(min(data)), max(data))
        if delta == 0:
            delta = 1

        # max_delta * scale = __max_y_pos / 2
        y_scale = (plot_y_size // 2) / delta
        # plot_y_scale half because negative part of graph is half the graph!!!!
        x = corner.x + 10
        prev = None
        pygame.draw.line(sim.window.pygame_scene, (41, 41, 41),
                         (corner.x, current_plot * plot_y_size + plot_y_size // 2),
                         (sim.window.width, current_plot * plot_y_size + plot_y_size // 2), width=5)
        for index in range(len(data) - 1, len(data) - sim.window.width - int(corner.x), -1):
            if index < 0:
                current = prev
            else:
                current = (x, (current_plot + 1) * plot_y_size - (y_scale * data[index]) - plot_y_size // 2)
                # top of plot size - y value (y is inverted)
            x = x + 1
            if prev is None:
                if current is None:
                    continue
                pygame.draw.line(sim.window.pygame_scene, (255, 0, 0), current, current, width=2)
            else:
                pygame.draw.line(sim.window.pygame_scene, (255, 0, 0), prev, current, width=2)
            prev = current

        sim.window.pygame_scene.blit(rendered, rect)
        sim.window.pygame_scene.blit(value_rendered, value_rect)
        pygame.draw.line(sim.window.pygame_scene, (255, 255, 255), (corner.x, (current_plot + 1) * plot_y_size),
                         (sim.window.width, (current_plot + 1) * plot_y_size), width=5)
        # Dont need big white line at the top so current_plot + 1
        # Draw upper line again, trace might have interfered with upper line
        pygame.draw.line(sim.window.pygame_scene, (255, 255, 255), (corner.x, current_plot * plot_y_size),
                         (sim.window.width, current_plot * plot_y_size), width=5)
        # Middle line

        current_plot = current_plot + 1
        if current_plot >= plots:
            break

    pygame.draw.line(sim.window.pygame_scene, (255, 255, 255), (corner.x, corner.y), (corner.x, sim.window.height),
                     width=10)


def _font(text: str, color: Tuple[int, int, int]) -> pygame.Surface:
    """
    Generate the rendered font or return a cached one
    :param text: The text to render
    :param color: The color of the text
    :return: The rendered font
    """
    if text in _font_cache:
        return _font_cache[text]
        # Dont even check if it has the correct color. It has.
    return sim.font.small_font.render(text, True, color, (0, 0, 0))
