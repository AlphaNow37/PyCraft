import pygame
from ...tools import get_size
from ... import Game

# the same render module as the others inventory, ...
from ...interfaces.unpaused_interfaces.widgets import grid_container
from ... import roots

class HotBarManager:
    w_path = roots.SRC_ROOT / "gui" / "widgets.png"
    widgets_surface = pygame.image.load(w_path)
    bar_surface = widgets_surface.subsurface([0, 0, 182, 22])

    hand_position_surface = widgets_surface.subsurface([0, 22, 24, 24])

    base_surface = pygame.Surface((bar_surface.get_width()+2, bar_surface.get_height()+2))
    base_surface.fill("#123456")  # Random color
    base_surface.set_colorkey("#123456")
    base_surface.blit(bar_surface, (1, 1))

    sizes_ratio = base_surface.get_width() / base_surface.get_height()

    def __init__(self, game):
        self.game: Game = game
        self.hotbar_viewer = grid_container.GridContainer(game, None, 9, 4, 4, 4, 16)
        self.box = pygame.Rect(0, 0, 0, 0)

    def draw(self):
        surface = self.base_surface.copy()
        surface.blit(self.hand_position_surface, (20*self.game.player_inventory.hand_position, 0))
        self.hotbar_viewer.draw(surface, self.game.player_inventory.inventory[:9])
        w_screen, h_screen = self.game.size_screen
        width, height = get_size(w_screen, h_screen, self.sizes_ratio, 1/2, 1/10)
        x = (w_screen-width)/2
        y = h_screen-height
        surface = pygame.transform.scale(surface, (int(width), int(height)))
        self.game.screen.blit(surface, [x, y])

        self.box.x = x
        self.box.y = y
        self.box.width = width
        self.box.height = height
