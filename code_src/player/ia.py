from ..entity import EntityIA
from ..constants import GameMode
from . import player


class PlayerIA(EntityIA):

    def __init__(self, game, entity):
        super().__init__(game, entity)
        self.entity: player.Player = entity

    def handle_player_inputs(self, pressed_keys, is_pressed_method):
        if is_pressed_method(pressed_keys, "left"):
            self.entity.move(-1, 0)
        if is_pressed_method(pressed_keys, "sneak"):
            self.entity.move(0, -1)
        if is_pressed_method(pressed_keys, "right"):
            self.entity.move(1, 0)
        if is_pressed_method(pressed_keys, "sneak") != self.entity.sneaking:
            if self.game.gamemode != GameMode.SPECTATOR:
                self.entity.set_sneaking(is_pressed_method(pressed_keys, "sneak"))

    def tick(self):
        pass
