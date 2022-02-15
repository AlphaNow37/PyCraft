from ... import Game
from . import HealthBar


class PlayerBarManager:
    def __init__(self, game: Game):
        self.game = game
        self.player = self.game.player
        self.health_bar_manager = HealthBar.HealthBarManager(game, self)

    def draw(self):
        if not self.game.is_admin:
            self.health_bar_manager.draw()
