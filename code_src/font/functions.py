import pygame
from .loader import unicode_letters, FONTSIZE, invalid_caracter, ascii_chars, ASCII_FONTSIZE

WIDTHCHAR = FONTSIZE - 8

def get_surface_from_ascii(line: str):
    surface = pygame.Surface((len(line)*(ASCII_FONTSIZE-2), ASCII_FONTSIZE))
    for x, char in enumerate(line):
        char_surface = ascii_chars[ord(char)].to_surface()
        surface.blit(char_surface, (x*(ASCII_FONTSIZE-2), 0))
    return surface

def get_surface_letter(letter: str, textcolor="white") -> pygame.Surface:
    page_id, x = divmod(ord(letter), 0xff)
    page_lst = unicode_letters.get(page_id)
    if page_lst is None:
        char = invalid_caracter
    else:
        char = page_lst[x]
    surface = char.to_surface(setcolor=textcolor, unsetcolor="#000000")
    # if page_id > 5:
    #     print(letter, hex(page_id), x, divmod(x, 16))
    #     pygame.show(surface)
    #     exit()
    return surface

def get_surface_line(phrase: str, textcolor="white", bg_color="black"):
    surface = pygame.Surface((WIDTHCHAR*len(phrase), FONTSIZE))
    surface.fill(bg_color)
    for x, letter in enumerate(phrase):
        letter_surface = get_surface_letter(letter, textcolor=textcolor)
        surface.blit(letter_surface, (x*WIDTHCHAR, 0))
    return surface
