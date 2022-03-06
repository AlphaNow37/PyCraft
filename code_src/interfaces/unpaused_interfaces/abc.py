from ..abc import AbcInterface

import pygame


class BaseUnpausedInterface(AbcInterface):
    paused = False
    surface: pygame.Surface

    def __init__(self, game):
        super().__init__(game)

    def tick(self):
        pass

    def draw(self):
        screen_w, screen_h = self.game.size_screen
        src_w, src_h = self.surface.get_size()
        coef = min(screen_w/src_w, screen_h/src_h)*0.8
        my_height = int(coef * src_w)
        my_width = int(coef * src_h)
        my_x = int((screen_w-my_width) / 2)
        my_y = int((screen_h-my_height) / 2)
        my_surface = pygame.transform.scale(self.get_surface(), (my_width, my_height))

        self.game.screen.blit(my_surface, [my_x, my_y, my_width, my_height])

    def get_surface(self) -> pygame.Surface:
        return self.surface

    def on_event(self, event):
        if event.type == pygame.KEYDOWN and event.key == pygame.K_e:
            self.game.interface = None
