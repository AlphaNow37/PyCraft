from ..abc import AbcInterface
from ...tools import get_size
from .widgets.grid_container import GridContainer
from ...container import Stack

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
        self.on_mouse_stack: Stack | None = None

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

        if self.on_mouse_stack is not None:
            stack_surface = self.on_mouse_stack.get_img()
            w = my_width / src_w * (16+3)
            h = my_height / src_h * 16
            stack_surface = pygame.transform.scale(stack_surface, (w, h))
            x_pos, y_pos = pygame.mouse.get_pos()
            self.game.screen.blit(stack_surface, (x_pos-w//2, y_pos-h//2))

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
            grid, pos = self.get_grid_from_xy(raw_x, raw_y)
            if grid is None:
                return
            at = grid.container[pos]
            if not grid.can_pose_items and self.on_mouse_stack:
                return
            if not grid.can_take_items and not self.on_mouse_stack:
                return
            grid.container[pos], self.on_mouse_stack = self.on_mouse_stack, at

    def get_grid_from_xy(self, raw_x, raw_y) -> tuple[GridContainer | None, int]:
        x, y = self.get_xy_from_rawpos(raw_x, raw_y)
        for grid in self.grids:
            if (pos := grid.get_xy_from_rawpos(x, y)) is not None:
                return grid, pos
        return None, -1

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
        if self.on_mouse_stack is not None:
            self.game.player_inventory.drop_item_or_stack(self.on_mouse_stack)
        for grid in self.grids:
            if grid.ephemeral_container:
                for stack in grid.container:
                    if stack is not None:
                        self.game.player_inventory.drop_item_or_stack(stack)
        super().close()
