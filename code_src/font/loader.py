from ..roots import SRC_ROOT
import pygame


letters_surface = pygame.image.load(SRC_ROOT / "ascii.png", )
FONTSIZE = 8
letters: list[list[pygame.mask.Mask]] = [
    [
        pygame.mask.from_surface(
            letters_surface.subsurface([x*FONTSIZE, y*FONTSIZE, FONTSIZE, FONTSIZE])
        ) for x in range(16)
    ] for y in range(16)
]
