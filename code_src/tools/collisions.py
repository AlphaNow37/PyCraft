from .. import Game
import pygame


def get_propertie_at(game: Game, prop_name, x, y, width=1, height=1, default=None):
    map_ = game.map
    self_rect = pygame.Rect((x - width / 2) * 100, (y - height / 2) * 100, width * 100, height * 100)
    for x_ in range(-2, 3):
        for y_ in range(-2, 3):
            block = map_.get_case(x + x_, y + y_)
            if (block is not None  # Valid case
                    and getattr(block, prop_name, False)  # has the propertie
                    and block.get_rect().colliderect(self_rect)):  # touch the player
                return getattr(block, prop_name)
    return default
