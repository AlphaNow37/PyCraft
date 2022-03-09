import pygame

from .guy_loader import load_guy_surface
from .abc import BaseUnpausedInterface
from .widgets import grid_container


_raw_surface = load_guy_surface("inventory")


class InventoryInterface(BaseUnpausedInterface):
    surface = _raw_surface.subsurface([0, 0, 176, 166]).copy()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.inventory = self.game.player_inventory.inventory
        self.top_container_grid = grid_container.GridContainer(
            self.game, None,
            9, 8, 84, 2, 16)
        self.hotbar = grid_container.GridContainer(
            self.game, None,
            9, 8, 142, 2, 16)

    def get_surface(self) -> pygame.Surface:
        surface = super().get_surface().copy()
        self.top_container_grid.draw(surface, self.inventory[9:])
        self.hotbar.draw(surface, self.inventory[:9])
        return surface
