import pygame
from .blocks import Block, blocks


class Ore(Block):
    fond = pygame.image.load("src/blocks/stones/stone.png")

    def __init__(self, name, game, x, y, name_fond, **kwargs):
        self.fond = blocks[name_fond]["img"]
        super(Ore, self).__init__(name, game, x, y, **kwargs)

    def draw(self, x_self=None, y_self=None, img=None, width=None, height=None):
        if self.revelated or self.game.is_admin:
            super().draw(x_self=x_self, y_self=y_self, img=self.img, width=width, height=height)
        else:
            super().draw(x_self=x_self, y_self=y_self, img=self.fond, width=width, height=height)
