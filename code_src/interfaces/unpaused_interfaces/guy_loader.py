import pygame
from ...roots import SRC_ROOT
guy_root = SRC_ROOT / "guy"


def load_guy_surface(name):
    return pygame.image.load(guy_root / f"{name}.png")
