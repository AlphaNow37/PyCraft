from ..roots import SRC_ROOT
import pygame

font_root = SRC_ROOT / "font"
FONTSIZE = 16
unicode_letters = {}
for page_id in range(0xff):
    path = font_root / f"unicode_page_{page_id:02x}.png"
    if not path.exists():
        continue
    surface = pygame.image.load(path)
    unicode_letters[page_id] = [
        pygame.mask.from_surface(
                surface.subsurface([x*FONTSIZE, y*FONTSIZE, FONTSIZE, FONTSIZE])
        )
        for y in range(16)
        for x in range(16)
    ]
unicode_letters[0][ord(" ")] = pygame.mask.Mask((1, 1))
invalid_caracter = unicode_letters[0][ord("?")]


ASCII_FONTSIZE = 8
_ascii_surface = pygame.image.load(font_root / "ascii.png")
ascii_chars = [
        pygame.mask.from_surface(
                _ascii_surface.subsurface([x*ASCII_FONTSIZE, y*ASCII_FONTSIZE, ASCII_FONTSIZE, ASCII_FONTSIZE])
        )
        for y in range(16)
        for x in range(16)
    ]
