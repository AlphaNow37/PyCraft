import math

from .base_entity import BaseEntity


class DirectedEntity(BaseEntity):
    def __init__(self, game, x, y, direction, degrees=True, **kwargs):
        super().__init__(game, x, y, **kwargs)
        self.set_dir(direction, degrees)

    def tick(self):
        x = self.x_speed * self.speed
        y = self.y_speed * self.speed
        super().move(x, y)
        super().tick()

    def set_dir(self, newdir, degrees=True):
        if degrees:
            newdir = math.radians(newdir)
        self.x_speed = math.sin(newdir)
        self.y_speed = math.cos(newdir)
