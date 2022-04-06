from ..base_elements import BaseImageCentree, RotatedImage
from ..constants import *
from ..tools import get_propertie_at
from .entity_ia import EntityIA


class BaseEntity(BaseImageCentree):
    collision = True
    fall = True
    speed = 0.5
    act_speed_y = 0
    destroy_after = None
    group = None

    name = "An entity"
    does_send_death_msg = False

    ia_cls = EntityIA

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.was_destroyed = False
        self.ia: EntityIA = self.ia_cls(self.game, self)

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
        """Return True if there is a collision"""
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
                self.event("FALLING_COLLISION", self.act_speed_y)
                self.act_speed_y = 0
        else:
            self.act_speed_y = 0
        if self.destroy_after is not None:
            if self.destroy_after <= 0:
                self.destroy()
            else:
                self.destroy_after -= 1
        if self.y < -50:
            self.event("VOID_DAMAGE")
        self.ia.tick()

    def get_down_block(self):
        x, y = self.get_int_pos()
        return self.map.get_case(x, y-1)

    def destroy(self):
        if not self.was_destroyed:
            self.was_destroyed = True
            group = self.group or self.game.entities
            group.remove(self)

    def event(self, name: str, *args):
        if name == "DEATH":
            self.destroy()
        elif name == "VOID_DAMAGE":
            self.destroy()

    def send_death_message(self, message: str):
        self.game.chat_manager.send(f"[Death] {message}")


class Mob(BaseEntity):
    base_life = 100
    parts: list[RotatedImage] = []

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._life = self.base_life

    def event(self, name: str, *args):
        if name == "VOID_DAMAGE":
            self.life -= 5
            if self.was_destroyed and self.does_send_death_msg:
                self.send_death_message(f"{self.name} fall into the void")
        elif name == "FALLING_COLLISION":
            speed, = args
            if speed < -1.5:
                self.life -= (-speed - 0.5) * 15
                if self.was_destroyed and self.does_send_death_msg:
                    self.send_death_message(f"{self.name} hits the ground too hard")
                    self.was_destroyed = False
        else:
            super().event(name, *args)

    def draw(self, x_self=None, y_self=None, img=None, width=None, height=None, frame=None):
        super().draw(x_self, y_self, img, width, height, frame)
        x = x_self if x_self is not None else self.x
        y = y_self if y_self is not None else self.y
        for part in self.parts:
            part.draw(x+part.x, y+part.y)

    @property
    def life(self):
        return self._life

    @life.setter
    def life(self, value):
        self._life = value
        if value <= 0:
            self.event("DEATH")
        else:
            self.event("LIFE_CHANGE")
