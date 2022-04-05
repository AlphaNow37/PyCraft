from .. import Game
from . import base_entity


class EntityIA:
    def __init__(self, game, entity):
        self.game: Game = game
        self.entity: base_entity.BaseEntity = entity

    def tick(self):
        pass
