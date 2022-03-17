import pygame

from ..entity import DirectedEntity
from . import item

import random
import math


class DroppedItem(DirectedEntity):
    destroy_after = 20 * 10
    width = 0.6
    height = 0.6

    def __init__(self, game, x, y, raw_item, **kwargs):
        super(DroppedItem, self).__init__(game, x, y, random.randint(0, 360), **kwargs)
        self.item: item.Item = item.get_item(raw_item)
        img = self.item.img
        w, h = img.get_size()
        self.img = pygame.Surface((w*2, h*2))
        self.img.blit(img, (w//2, h//2))
        self.img.set_colorkey("black")

    def tick(self):
        self.x_speed *= 0.99
        self.y_speed *= 0.99
        super().tick()
        dist = math.dist(self.game.player.pos, self.pos)
        if dist < 1:
            if not self.game.player_inventory.take_item(self.item):
                self.destroy()
                print("objet ramassé")
        elif dist < 3:
            self.collision = False
            self.fall = False
            x, y = self.game.player.pos
            x -= self.x
            y -= self.y
            self.x_speed = x/5
            self.y_speed = y/5
        else:
            if not self.fall:
                self.x_speed = 0
                self.y_speed = 0
            self.collision = True
            self.fall = True
