from ..base_elements import BaseCarre
import pygame
from .. import Game
from ..blocks import Block
from ..constants import PLAYER_RANGE
from ..roots import SRC_ROOT


class Breaker(BaseCarre):
    imgs = [pygame.image.load(SRC_ROOT / "misc" / "destroy" / f"destroy_stage_{i}.png") for i in range(10)]


class BreakerPlacerManager:
    """Gere certaines interactions (placer et casser des blocks a la main)"""
    def __init__(self, game: Game):
        self.breaker = Breaker(game, 0, 0)
        self.reset()
        self.game = game
        self.map = game.map

    def tick(self):
        if self.game.interface is not None:
            self.reset()
            return
        left, _, right = pygame.mouse.get_pressed(3)
        mouse_pos = self.game.mouse_pos
        x, y = mouse_pos
        block = self.map.get_case(x, y)

        if block is not None and self.game.player.get_distance(x, y) <= self.get_player_range():
            if block.air:
                if right:
                    if self.game.is_admin:
                        ok = True
                    else:
                        ok = any(not block_next.air for block_next in self.map.get_around(x, y))
                    if ok:
                        x_side, y_side = self.game.block_side
                        block = Block("stone", self.game, x, y)
                        if block.support_x_flip:
                            block.flip_x = x_side < 0.5
                        if block.support_y_flip:
                            block.flip_y = y_side < 0.5
                        self.map.set_case(x, y, block)
                        self.game.sound_manager.placed(block.breaked_sound)
            else:
                if block.unbreakable:
                    if self.game.is_admin and left:
                        self.map.destroy_case(x, y)
                    else:
                        self.reset()
                elif left and mouse_pos == self.breaking_pos and self.breaking:
                    pass
                elif left:
                    self.breaking = True
                    self.stage = 0
                    self.breaking_pos = mouse_pos
                    self.rest_breaking_solidity = block.solidity
                else:
                    self.breaking = False
                if self.breaking:
                    self.rest_breaking_solidity -= self.game.player.get_mining_speed(block.outil)/25
                    if self.rest_breaking_solidity <= 0:
                        self.map.destroy_case(x, y, do_drop=True)
                    else:
                        self.stage = 10-int(self.rest_breaking_solidity/block.solidity*10)
                        if self.stage != self.last_stage:
                            self.game.sound_manager.breaked(block.breaked_sound, sleep=True)
                            self.last_stage = self.stage
                        return
        self.reset()

    def reset(self):
        self.breaking = False
        self.stage = 0
        self.breaking_pos = (None, None)
        self.rest_breaking_solidity = None
        self.last_stage = None

    def draw(self):
        if self.breaking:
            self.breaker.x, self.breaker.y = self.breaking_pos
            self.breaker.frame = self.stage//2
            self.breaker.frame %= len(self.breaker.imgs)
            self.breaker.draw()
        return self.breaking

    def get_player_range(self):
        return float("inf") if self.game.is_admin else PLAYER_RANGE
