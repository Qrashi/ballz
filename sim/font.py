import pygame

font: pygame.font = None


def init():
    print("O Initializing fonts...", end = "")
    pygame.font.init()
    print("\r\033[K\rO Loading roboto...", end = "")
    font = pygame.font.SysFont("asd", 20)
    print(f"\r\033[K\r✓ Font loading complete")
