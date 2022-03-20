from .roots import SRC_ROOT
import pygame


letters_surface = pygame.image.load(SRC_ROOT / "ascii.png", )

letters = [
    [
        letters_surface.subsurface([x*8, y*8, 8, 8])
        for x in range(16)
    ] for y in range(16)
]

def get_surface_letter(letter: str):
    y, x = divmod(ord(letter), 16)
    return letters[y][x]

def get_surface_line(phrase: str):
    surface = pygame.Surface((8*len(phrase), 8))
    surface.set_colorkey("black")
    for x, letter in enumerate(phrase):
        letter_surface = get_surface_letter(letter)
        surface.blit(letter_surface, (x*8, 0))
    return surface
