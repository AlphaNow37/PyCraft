import pygame.transform

from ... import Game
from . import icons
from . import __init__


class HealthBarManager:
    def __init__(self, game: Game, manager):
        self.game = game
        empty_surface = icons.load_basic_icon(0, 0)
        self.hearth_surfaces = {
            name: [src := empty_surface.copy(), src.blit(icons.load_basic_icon(x, y), (0, 0))][0]
            for (name, x, y) in [("plain", 4, 0), ("partial", 5, 0), ("empty", 0, 0)]
        }
        self.super_manager: __init__.PlayerBarManager = manager

    def draw(self):
        w, h = self.game.size_screen
        height_hearth = min(w/50, h/10)
        life = self.game.player.life
        nb_heath, nb_partial_heath = divmod(life, 10)
        nb_partial_heath = 1 if nb_partial_heath else 0
        hearths_surfaces = {
            name: pygame.transform.scale(surface, (height_hearth, height_hearth))
            for (name, surface) in self.hearth_surfaces.items()
        }
        for i in range(max(nb_heath+nb_partial_heath, 10)):
            y, x = divmod(i, 10)
            screen_x = x * height_hearth
            screen_y = y * height_hearth
            if i < nb_heath:
                name = "plain"
            elif i == nb_heath and nb_partial_heath == 1:
                name = "partial"
            else:
                name = "empty"
            if name is not None:
                self.game.screen.blit(hearths_surfaces[name], (screen_x, screen_y))
