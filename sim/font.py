import pygame

font: pygame.font = None

def init():
    print("O Initializing fonts...", end = "")
    pygame.font.init()
    print("\r\x1b[2K\rO Loading roboto...", end = "")
    font = pygame.font.SysFont("asd", 20)
    print(f"\r\x1b[2K\r✓ Font loading complete")
