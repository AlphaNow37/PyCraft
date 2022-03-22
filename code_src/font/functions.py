import pygame
from .loader import letters, FONTSIZE


def get_surface_letter(letter: str, textcolor="white") -> pygame.Surface:
    y, x = divmod(ord(letter), 16)
    return letters[y][x].to_surface(setcolor=textcolor, unsetcolor="#000000")

def get_surface_line(phrase: str, textcolor="white"):
    surface = pygame.Surface((FONTSIZE*len(phrase), FONTSIZE))
    surface.set_colorkey("black")
    for x, letter in enumerate(phrase):
        letter_surface = get_surface_letter(letter, textcolor=textcolor)
        surface.blit(letter_surface, (x*FONTSIZE, 0))
    return surface
