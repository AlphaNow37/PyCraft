from ... import Game
from . import HealthBar


class PlayerBarManager:
    def __init__(self, game: Game):
        self.game = game
        self.player = self.game.player
        self.heath_bar_manager = HealthBar.HealthBarManager(game, self)

    def draw(self):
        self.heath_bar_manager.draw()
