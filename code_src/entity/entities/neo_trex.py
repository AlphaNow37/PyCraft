from .. import BaseEntity
from ... import roots
import random

import pygame

MAX_TRIES = 10


class NeoTRex(BaseEntity):
    img = pygame.image.load(roots.SRC_ROOT / "entity" / "NeoTrex.png")

    going_right = bool(random.getrandbits(1))
    base_life = float("inf")
    n_collision_before_turn = MAX_TRIES
    flip_x = not going_right

    def tick(self):
        x = 0.1 if self.going_right else -0.1
        has_collsion, _ = self.move(x, 0)
        if has_collsion:
            self.n_collision_before_turn -= 1
            if self.n_collision_before_turn == 0:
                self.going_right = not self.going_right
                self.flip_x = not self.going_right
                self.n_collision_before_turn = MAX_TRIES
            else:
                self.act_speed_y += 0.2
        else:
            self.n_collision_before_turn = MAX_TRIES
        super().tick()
