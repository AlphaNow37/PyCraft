from .. import Mob
from ... import roots
from ..IAs import BasicMobIA

import pygame


class NeoTRex(Mob):
    img = pygame.image.load(roots.SRC_ROOT / "entity" / "NeoTrex.png")
    base_life = float("inf")
    ia_cls = BasicMobIA
    ia: BasicMobIA
