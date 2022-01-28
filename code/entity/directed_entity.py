import math
from .base_entity import BaseEntity


class DirectedEntity(BaseEntity):
    def __init__(self, game, x, y, direction, degrees=True, **kwargs):
        super().__init__(game, x, y)
        self.direction = direction
        if degrees:
            self.direction = math.radians(self.direction)

    def tick(self):
        x = math.sin(self.direction) * self.speed
        y = math.cos(self.direction) * self.speed
        super().move(x, y)
        super().tick()
