import string

import pygame
from .loader import FONTSIZE
from .functions import get_surface_letter
from .colors import clr, id_to_hex


HEIGHTLINE = FONTSIZE + 1
COLOUR_CHANGE_TOKEN = "§"

def get_text(text, alpha=70, default_textcolor="white", background_color="black"):
    lines = [list(line) for line in text.splitlines()]

    # Get maximum width and parsing the colors
    max_width = 0
    for line in lines:
        x = 0
        width = 0
        while x < len(line):
            if line[x] == "§" and x != len(line)-1:
                if line[x+1] == "#":
                    line[x] = "".join(map(str.lower, line[x+1:x+8]))
                    del line[x+1:x+8]
                elif line[x+1] in string.hexdigits:
                    line[x] = "#"+id_to_hex[line[x+1]]
                    del line[x+1]
                else:
                    width += 1
            else:
                width += 1
            x += 1
        if width > max_width:
            max_width = width

    # Creating the surface
    height = len(lines)
    surface = pygame.Surface((max_width*FONTSIZE, height*(FONTSIZE+1)-1))
    surface.fill(background_color)

    # Bliting all the characters
    textcolor = default_textcolor
    for y, line in enumerate(lines):
        x = 0
        while x < len(line):
            at = line[x]
            if len(at) == 1:
                char_surface = get_surface_letter(at, textcolor)
                surface.blit(char_surface, (x*FONTSIZE, y*(FONTSIZE+1)))
                x += 1
            else:
                textcolor = at
                del line[x]

    # Returning the surface
    surface.set_alpha(alpha)
    return surface

pygame.show(get_text(f"aaa{clr:blue}bbb\n§1ccc", default_textcolor="red"))
exit()
