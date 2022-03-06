from .guy_loader import load_guy_surface
from .abc import BaseUnpausedInterface


_raw_surface = load_guy_surface("inventory")


class InventoryInterface(BaseUnpausedInterface):
    surface = _raw_surface.subsurface([0, 0, 176, 166]).copy()
