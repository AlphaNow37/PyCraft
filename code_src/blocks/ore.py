import pygame
from .blocks import Block, blocks


class Ore(Block):
    """Classe de tous les minerais"""
    fond = pygame.image.load("src/blocks/stones/stone.png")
    revelated = False

    def __init__(self, name, game, x, y, name_fond, **kwargs):
        self.fond = blocks[name_fond]["img"]
        self.name_fond = name_fond
        super(Ore, self).__init__(name, game, x, y, **kwargs)
        self.base_img = self.img

    def draw(self, *args, **kwargs):
        if self.revelated or self.game.is_admin:
            super().draw(*args, **kwargs, img=self.base_img)
        else:
            super().draw(*args, **kwargs, img=self.fond)
