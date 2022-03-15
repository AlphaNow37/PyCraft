from ..abc import AbcInterface
from ...tools import get_size
from .widgets.grid_container import GridContainer

import pygame


class BaseUnpausedInterface(AbcInterface):
    paused = False
    surface: pygame.Surface

    grids: list[GridContainer] = []
    last_rect: pygame.Rect
    last_surfacesize: tuple[int, int]

    def __init__(self, game):
        self.grids = []
        super().__init__(game)

    def tick(self):
        pass

    def draw(self):
        screen_w, screen_h = self.game.size_screen
        src_w, src_h = self.surface.get_size()
        self.last_surfacesize = src_w, src_h
        my_width, my_height = get_size(screen_w, screen_h, src_w/src_h*1, 0.8, 0.8)
        my_x = int((screen_w-my_width) / 2)
        my_y = int((screen_h-my_height) / 2)
        my_surface = pygame.transform.scale(self.get_surface(), (my_width, my_height))
        self.last_rect = pygame.Rect(my_x, my_y, my_width, my_height)
        self.game.screen.blit(my_surface, self.last_rect)

    def get_surface(self) -> pygame.Surface:
        surface = self.surface.copy()
        for grid in self.grids:
            grid.draw(surface)
        return surface

    def on_event(self, event):
        if event.type == pygame.KEYDOWN and event.key == pygame.K_e:
            self.close()
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == pygame.BUTTON_LEFT:
            raw_x, raw_y = event.pos
            x, y = self.get_xy_from_rawpos(raw_x, raw_y)
            for grid in self.grids:
                if (pos := grid.get_xy_from_rawpos(x, y)) is not None:
                    print(pos)

    def get_xy_from_rawpos(self, x, y):
        x -= self.last_rect.x
        y -= self.last_rect.y
        x /= self.last_rect.width
        y /= self.last_rect.height
        x *= self.last_surfacesize[0]
        y *= self.last_surfacesize[1]
        return x, y

    def close(self):
        print("interface closed")
        super().close()
