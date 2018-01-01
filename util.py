import pygame

def scale(surface, rate):
    width = surface.get_width()
    height = surface.get_height()
    return pygame.transform.scale(surface, (width * rate, height * rate))
