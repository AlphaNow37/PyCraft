from ...constants import SRC_ROOT
import pygame

icons_path = SRC_ROOT / "guy" / "icons.png"
icons_surface = pygame.image.load(icons_path)

cursor_surface = icons_surface.subsurface([0, 0, 15, 15])

def load_basic_icon(x_grid, y_grid):
    x = 16 + 9*x_grid
    y = 9 * y_grid
    return icons_surface.subsurface([x, y, 9, 9])
