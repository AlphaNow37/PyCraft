from .guy_loader import load_guy_surface
from .abc import BaseUnpausedInterface
from .widgets import grid_container
from ...container import Container


_raw_surface = load_guy_surface("inventory")


class InventoryInterface(BaseUnpausedInterface):
    surface = _raw_surface.subsurface([0, 0, 176, 166]).copy()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # self.inventory = self.game.player_inventory.inventory
        self.top_container_grid = grid_container.GridContainer(
            self.game, self.game.player_inventory.upinventory,
            9, 8, 84, 2, 16)
        self.hotbar = grid_container.GridContainer(
            self.game, self.game.player_inventory.hotbar,
            9, 8, 142, 2, 16)
        self.crafter = grid_container.GridContainer(
            self.game, Container(4),
            2, 98, 18, 2, 16,
            ephemeral_container=True,
        )
        self.grids.append(self.hotbar)
        self.grids.append(self.top_container_grid)
        self.grids.append(self.crafter)

    # def get_surface(self) -> pygame.Surface:
    #     print(self.hotbar.container.grid)
    #     print(*self.hotbar.container)
    #     return super().get_surface()
    #     # surface = super().get_surface().copy()
    #     # self.top_container_grid.draw(surface, self.inventory[9:])
    #     # self.hotbar.draw(surface, self.inventory[:9])
    #     # return surface
