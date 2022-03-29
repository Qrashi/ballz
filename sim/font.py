import pygame

from utils import pool

print("O Loading font system", end="")
pygame.font.init()
print("\r\033[K\rO Loading " + pool.open("config.json").json["font"] + " size 100", end="")
main_font = pygame.font.SysFont(pool.open("config.json").json["font"], 100)
small_font_size = 50
print("\r\033[K\rO Loading " + pool.open("config.json").json["font"] + f" size {small_font_size}", end="")
small_font = pygame.font.SysFont(pool.open("config.json").json["font"], small_font_size)
print("\r\033[K\r✓ Font loading complete")
