import pygame

from ..entity import DirectedEntity
from .. import container

import random
import math


class DroppedItem(DirectedEntity):
    destroy_after = 20 * 10
    width = 19 * 3/100
    height = 16 * 3/100

    def __init__(self, game, x, y, raw_item, direction=None, *, time_cant_be_taked=0, isblock=False, **kwargs):
        direction = random.randint(0, 360) if direction is None else direction
        super(DroppedItem, self).__init__(game, x, y, direction, **kwargs)
        self.stack = container.Stack.new(raw_item, is_block=isblock)
        img = self.stack.get_img()
        w, h = img.get_size()
        self.img = pygame.Surface((w*2, h*2))
        self.img.blit(img, (w//2, h//2))
        self.img.set_colorkey("black")
        self.time_cant_be_taked = time_cant_be_taked

    def tick(self):
        self.x_speed *= 0.99
        self.y_speed *= 0.99
        super().tick()
        dist = math.dist(self.game.player.pos, self.pos)
        if self.time_cant_be_taked > 0:
            self.time_cant_be_taked -= 1
        elif dist < 1:
            if not self.game.player_inventory.take_item(self.stack):
                self.destroy()
            return
        elif dist < 3:
            self.collision = False
            self.fall = False
            x, y = self.game.player.pos
            x -= self.x
            y -= self.y
            self.x_speed = x/5
            self.y_speed = y/5
            return
        if not self.fall:
            self.x_speed = 0
            self.y_speed = 0
        self.collision = True
        self.fall = True
