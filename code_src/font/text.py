import string

import pygame
from .loader import FONTSIZE
from .functions import get_surface_letter
from .colors import clr, id_to_hex, get_color_from_name


HEIGHTLINE = FONTSIZE + 1
WIDTHCHAR = FONTSIZE - 8
COLOUR_CHANGE_TOKEN = "§"

basic_chars = {
    "_": "__",
    "-": "--",
    "n": "__",
    "m": "--",
    "r": "//",
}

def get_text(text, alpha=70,
             default_textcolor="white", background_color="black",
             padx=0, pady=0,
             maxlinesize: int | None = None):
    """Return a surface with the text.
    Support color codes."""

    # Applying the maximum size of a line
    if maxlinesize is not None:
        str_lines = _cut_text(text, maxlinesize)
        lines: list[list[str]] = [list(line) for line in str_lines]
    else:
        lines: list[list[str]] = [list(line) for line in text.splitlines()]

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
                elif line[x+1] == "{":
                    x2 = x+1
                    content = ""
                    while True:
                        x2 += 1
                        if x2 >= len(line):
                            break
                        elif line[x2] == "}":
                            try:
                                line[x] = get_color_from_name(content)[1:]
                            except ValueError:
                                width += 1
                            else:
                                del line[x+1:x2+1]
                            break
                        else:
                            content += line[x2]
                elif line[x+1] in basic_chars:
                    line[x] = basic_chars[line[x+1]]
                    del line[x+1]
                else:  # aaa§{blue}bbb
                    width += 1
            else:
                width += 1
            x += 1
        if width > max_width:
            max_width = width

    # Creating the surface
    height = len(lines)
    surface = pygame.Surface((max_width*WIDTHCHAR+padx*2, height*HEIGHTLINE+padx*2))
    surface.fill(background_color)

    # Bliting all the characters
    textcolor = default_textcolor
    barre = False
    underline = False
    for y, line in enumerate(lines):
        x = 0
        while x < len(line):
            at = line[x]
            if len(at) == 1:  # Bliting the char
                left = x*WIDTHCHAR+padx
                top = y*HEIGHTLINE+pady
                char_surface = get_surface_letter(at, textcolor)
                surface.blit(char_surface, (left, top))
                if barre:
                    y_ = top+FONTSIZE//2
                    pygame.draw.line(surface, textcolor, (left, y_), (left+WIDTHCHAR, y_))
                if underline:
                    y_ = top+FONTSIZE+1
                    pygame.draw.line(surface, textcolor, (left, y_), (left+WIDTHCHAR, y_))
                x += 1
            elif at.startswith("#"):  # changing textcolor
                textcolor = at
                del line[x]
            elif at == "--":  # barre
                barre = not barre
                del line[x]
            elif at == "__":  # underline
                underline = not underline
                del line[x]
            elif at == "//":  # reset
                textcolor = default_textcolor
                barre = False
                underline = False
                del line[x]
            else:
                raise

    # Returning the surface
    surface.set_alpha(alpha)
    return surface


def _cut_text(text: str, maxlinesize: int) -> list[str]:
    """Add \n to have line with :maxlinesize: lenght"""
    raw_lines = text.splitlines()
    cutted_lines = []
    for y, line in enumerate(raw_lines):
        worlds = line.split()
        x = 0
        act_line = ""
        while x < len(worlds):
            world = worlds[x]
            while world:
                if len(act_line) + len(world) > maxlinesize:
                    if act_line:
                        cutted_lines.append(act_line)
                        act_line = ""
                    else:
                        cutted_lines.append(world[:maxlinesize])
                        world = world[maxlinesize:]
                else:
                    act_line += world
                    if len(act_line) == maxlinesize:
                        cutted_lines.append(act_line)
                        act_line = ""
                    else:
                        act_line += " "
                    world = None
            x += 1
        cutted_lines.append(act_line)
    return [line.removesuffix(" ") for line in cutted_lines]

# pygame.show(get_text(f"aaa{clr:blue}bbb\n§1ccc", default_textcolor="red"))
# exit()
_TESTING = False
if _TESTING:
    print(_cut_text("aaa\nbonjour tout le monde !!! abcdefghi", 30))
    exit()
