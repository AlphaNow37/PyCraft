import pygame.image
from ...tools import get_size
from ... import Game

# the same render module as the others inventory, ...
from ...interfaces.unpaused_interfaces.widgets import grid_container
from ... import roots

class HotBarManager:
    w_path = roots.SRC_ROOT / "gui" / "widgets.png"
    widgets_surface = pygame.image.load(w_path)
    bar_surface = widgets_surface.subsurface([0, 0, 182, 22])
    sizes_ratio = bar_surface.get_width() / bar_surface.get_height()

    def __init__(self, game):
        self.game: Game = game
        self.hotbar_viewer = grid_container.GridContainer(game, None, 9, 3, 3, 4, 16)

    def draw(self):
        surface = self.bar_surface.copy()
        self.hotbar_viewer.draw(surface, self.game.player_inventory.inventory[:9])
        w_screen, h_screen = self.game.size_screen
        width, height = get_size(w_screen, h_screen, self.sizes_ratio, 1/2, 1/10)
        x = (w_screen-width)/2
        y = h_screen-height
        surface = pygame.transform.scale(surface, (int(width), int(height)))
        self.game.screen.blit(surface, [x, y])
