from .directed_entity import DirectedEntity
import random
import pygame
import math


class Particle(DirectedEntity):
    destroy_after = 20
    speed = 0.2
    collision = True
    width = 0.2
    height = 0.2
    fall = True

    def __init__(self, game, x, y, base_img: pygame.Surface, **kwargs):
        super().__init__(game, x, y, random.randint(-180, 180), **kwargs)
        width_img, height_img = base_img.get_size()
        width_sub = math.ceil(width_img/8)
        height_sub = math.ceil(height_img/8)
        left = random.randint(0, width_img-width_sub)
        top = random.randint(0, height_img-height_sub)
        self.img = base_img.subsurface(left, top, width_sub, height_sub)

    def tick(self):
        self.act_speed_y *= 0.9
        super().tick()
