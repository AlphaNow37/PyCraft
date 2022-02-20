import pygame

from ..base_elements import BaseImageCentree
from ..constants import *
from ..tools import get_propertie_at


class BaseEntity(BaseImageCentree):
    collision = True
    fall = True
    speed = 0.5
    act_speed_y = 0
    destroy_after = None
    base_life = 100

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._life = self.base_life
        self.was_destroyed = False

    def move(self, x, y) -> tuple[bool, tuple[float | int, ...]]:
        if self.collision:
            x_ = x/10
            y_ = y/10
            any_ = False
            for _ in range(10):
                if not self.verify_collision(self.x + x_, self.y + y_):
                    self.x += x_
                    self.y += y_
                    max_speed = get_propertie_at(self.game, "falling_max_speed", self.x, self.y, self.width, self.height)
                    if max_speed:
                        max_speed /= 10
                        y_ = max(y_, -max_speed)
                        x_ = max(min(x_, max_speed), -max_speed)
                else:
                    any_ = True
                    break
            return any_, (x_*10, y_*10)
        else:
            self.x += x
            self.y += y
            return False, (x, y)

    def verify_collision(self, x=None, y=None):
        if not self.collision:
            return False
        if x is None:
            x = self.x
        if y is None:
            y = self.y
        return get_propertie_at(self.game, "collision", x, y, self.width, self.height)

    def tick(self):
        self.was_destroyed = False
        self.act_speed_y -= GRAVITY
        if self.fall:
            any_, new_falling_speed = self.move(0, self.act_speed_y)
            self.act_speed_y = new_falling_speed[1]
            if any_:
                speed = self.act_speed_y
                if speed < -1.5:
                    self.life -= (-speed - 0.5) * 15
                self.act_speed_y = 0
        else:
            self.act_speed_y = 0
        if self.destroy_after is not None:
            if self.destroy_after <= 0:
                self.destroy()
            else:
                self.destroy_after -= 1
        if self.y < -50:
            self.life -= 5

    def get_down_block(self):
        x, y = self.get_int_pos()
        return self.map.get_case(x, y-1)

    def destroy(self):
        self.was_destroyed = True
        self.game.entity_manager.remove(self)

    @property
    def life(self):
        return self._life

    @life.setter
    def life(self, value):
        self._life = value
        if value <= 0:
            self.destroy()
            self.event("DEATH")
        else:
            self.event("LIFE_CHANGE")

    def event(self, name: str, *args):
        if name == "DEATH":
            self.destroy()
