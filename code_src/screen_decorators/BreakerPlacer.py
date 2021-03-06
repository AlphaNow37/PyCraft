from ..base_elements import BaseCarre
import pygame
from .. import Game
from ..blocks import Block, get_cls
from ..constants import PLAYER_RANGE
from ..roots import SRC_ROOT


class Breaker(BaseCarre):
    imgs = [pygame.image.load(SRC_ROOT / "misc" / "destroy" / f"destroy_stage_{i}.png") for i in range(10)]


class BreakerPlacerManager:
    """Gere certaines interactions (placer et casser des blocks a la main)"""
    def __init__(self, game: Game):
        self.breaker = Breaker(game, 0, 0)
        self.reset_breaking()
        self.game = game
        self.map = game.map

    def tick(self):
        if self.game.interface is not None:
            self.reset_breaking()
            return
        left, _, right = pygame.mouse.get_pressed(3)
        mouse_pos = self.game.mouse_pos
        x, y = mouse_pos

        # If the mouse is on the hotbar
        hotbar_manager = self.game.sc_deco.player_bar_manager.hotbar_manager
        if hotbar_manager.box.collidepoint(pygame.mouse.get_pos()):
            return

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
                        item = self.game.player_inventory.get_main_hand_item()
                        if item is not None and item.item_type == "block":
                            cls: type[Block] = get_cls(item.name)
                            block = cls.place_at(item.name, self.game, x, y)
                            if block is not False:
                                if block.support_x_flip:
                                    block.flip_x = x_side < 0.5
                                if block.support_y_flip:
                                    block.flip_y = y_side < 0.5
                                if not self.game.is_admin:
                                    self.game.player_inventory.remove_one_in_hand()
                                self.game.sound_manager.placed(block.breaked_sound)
            else:
                if block.unbreakable:
                    if self.game.is_admin and left:
                        self.map.destroy_case(x, y)
                    else:
                        self.reset_breaking()
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
                    self.rest_breaking_solidity -= self.game.player_inventory.get_mining_speed(block.outil)/25
                    if self.rest_breaking_solidity <= 0:
                        self.map.destroy_case(x, y, do_drop=True)
                    else:
                        self.stage = 10-int(self.rest_breaking_solidity/block.solidity*10)
                        if self.stage != self.last_stage:
                            self.game.sound_manager.breaked(block.breaked_sound, sleep=True)
                            self.last_stage = self.stage
                        return
        self.reset_breaking()

    def reset_breaking(self):
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
