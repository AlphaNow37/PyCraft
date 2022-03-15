from ..abc import AbcInterface
from ...tools import get_size
from .widgets.grid_container import GridContainer

import pygame


class BaseUnpausedInterface(AbcInterface):
    paused = False
    surface: pygame.Surface

    grids: list[GridContainer] = []

    def __init__(self, game):
        self.grids = []
        super().__init__(game)

    def tick(self):
        pass

    def draw(self):
        screen_w, screen_h = self.game.size_screen
        src_w, src_h = self.surface.get_size()
        my_width, my_height = get_size(screen_w, screen_h, src_w/src_h*1, 0.8, 0.8)
        my_x = int((screen_w-my_width) / 2)
        my_y = int((screen_h-my_height) / 2)
        my_surface = pygame.transform.scale(self.get_surface(), (my_width, my_height))

        self.game.screen.blit(my_surface, [my_x, my_y, my_width, my_height])

    def get_surface(self) -> pygame.Surface:
        surface = self.surface.copy()
        for grid in self.grids:
            grid.draw(surface)
        return surface

    def on_event(self, event):
        if event.type == pygame.KEYDOWN and event.key == pygame.K_e:
            self.close()

    def close(self):
        print("interface closed")
        super().close()
