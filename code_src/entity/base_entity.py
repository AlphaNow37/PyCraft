import pygame
from ..base_elements import BaseImageCentree
from ..constants import *


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

    def move(self, x, y):
        if self.collision:
            x_ = x/10
            y_ = y/10
            any_ = False
            for _ in range(10):
                if not self.get_collision(self.x+x_, self.y+y_):
                    self.x += x_
                    self.y += y_
                else:
                    any_ = True
                    break
            return any_
        else:
            self.x += x
            self.y += y
            return False

    def get_collision(self, x=None, y=None):
        if not self.collision:
            return False
        if x is None:
            x = self.x
        if y is None:
            y = self.y

        self_rect = pygame.Rect((x-self.width/2)*100, (y-self.height/2)*100, self.width*100, self.height*100)
        for x_ in range(-2, 3):
            for y_ in range(-2, 3):
                block = self.map.get_case(x+x_, y+y_)
                if block is not None and block.collision and block.get_rect().colliderect(self_rect):
                    return True
        return False

    def tick(self):
        self.act_speed_y -= GRAVITY
        if self.act_speed_y > 0:
            any_ = self.move(0, self.act_speed_y)
            if any_:
                self.act_speed_y = 0
        if self.fall:
            any_ = self.move(0, self.act_speed_y)
            if any_:
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
        self.game.entity_manager.remove(self)

    @property
    def life(self):
        return self._life

    @life.setter
    def life(self, value):
        self._life = value
        if value == 0:
            self.destroy()
        else:
            self.event("LIFE_CHANGE")

    def event(self, name: str, *args):
        pass
