"""
Responsible for font loading
"""
import pygame

import sim
from utils import pool

main_font: pygame.font.SysFont
small_font_size: int = 50
small_font: pygame.font.SysFont
normal_font_size: int = 100


def init():
    """
    Initialize all fonts and scale them appropriately
    """
    print("O Loading font system", end="")
    pygame.font.init()
    sim.font.small_font_size = sim.window.width // 70
    sim.font.normal_font_size = sim.window.width // 30
    print("\r\033[K\rO Loading " + pool.open("config.json").json["font"].lower() + f" size {sim.font.normal_font_size}", end="")
    sim.font.main_font = pygame.font.SysFont(pool.open("config.json").json["font"], sim.font.normal_font_size)
    print("\r\033[K\rO Loading " + pool.open("config.json").json["font"].lower() + f" size {sim.font.small_font_size}", end="")
    sim.font.small_font = pygame.font.SysFont(pool.open("config.json").json["font"], sim.font.small_font_size)
    print("\r\033[K\rOK Font loading complete!")
