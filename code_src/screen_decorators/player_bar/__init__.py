from ... import Game
from . import HealthBar
from . import Hotbar


class PlayerBarManager:
    def __init__(self, game: Game):
        self.game = game
        self.player = self.game.player
        self.health_bar_manager = HealthBar.HealthBarManager(game, self)
        self.hotbar_manager = Hotbar.HotBarManager(self.game)

    def draw(self):
        if not self.game.is_admin:
            self.health_bar_manager.draw()
        self.hotbar_manager.draw()

    def after_initialisation(self):
        self.hotbar_manager.after_initialisation()
