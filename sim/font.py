import pygame

from utils import pool

print("O Loading font system", end="")
pygame.font.init()
print("\r\033[K\rO Loading " + pool.open("config.json").json["font"], end="")
font = pygame.font.SysFont(pool.open("config.json").json["font"], 100)
print("\r\033[K\r✓ Font loading complete")
