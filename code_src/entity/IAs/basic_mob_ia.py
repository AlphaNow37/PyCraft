from ..entity_ia import EntityIA
import random

MAX_TRIES = 10


class BasicMobIA(EntityIA):
    going_right = bool(random.getrandbits(1))
    n_collision_before_turn = MAX_TRIES

    def tick(self):
        x = 0.1 if self.going_right else -0.1
        has_collsion, _ = self.entity.move(x, 0)
        if has_collsion:
            self.n_collision_before_turn -= 1
            if self.n_collision_before_turn == 0:
                self.going_right = not self.going_right
                self.flip_x = not self.going_right
                self.n_collision_before_turn = MAX_TRIES
            else:
                self.entity.act_speed_y += 0.2
        else:
            self.n_collision_before_turn = MAX_TRIES
        self.entity.flip_x = not self.going_right
