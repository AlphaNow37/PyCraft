import pygame

from ..entity import DirectedEntity
from .item import Item, get_item

import random
import math


class DroppedItem(DirectedEntity):
    destroy_after = 20 * 10
    width = 0.6
    height = 0.6

    def __init__(self, game, x, y, raw_item):
        super(DroppedItem, self).__init__(game, x, y, random.randint(0, 360))
        self.item: Item = get_item(raw_item)
        img = self.item.img
        w, h = img.get_size()
        self.img = pygame.Surface((w*2, h*2))
        self.img.blit(img, (w//2, h//2))
        self.img.set_colorkey("black")

    def tick(self):
        self.x_speed *= 0.99
        self.y_speed *= 0.99
        super().tick()
        if self.do_collide_player():
            self.destroy()
            print("objet ramassé")

    def do_collide_player(self):
        return math.dist(self.game.player.pos, self.pos) < 3
