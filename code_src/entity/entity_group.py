from .. import Game
from . import BaseEntity

from .entities import neo_trex


class EntityGroup:
    """Rassemble des entitéss"""
    def __init__(self, game: Game):
        self.game = game
        self.entity_lst: list[BaseEntity] = [neo_trex.NeoTRex(game, 0, game.player.y)]

    def tick(self):
        for entity in self.entity_lst:
            entity.tick()

    def draw(self):
        for entity in self.entity_lst:
            entity.draw()

    def add(self, *args, **kwargs):
        if len(args) == 1 and not kwargs and isinstance(args[0], BaseEntity):
            entity = args[0]
        else:
            cls = kwargs.pop("cls", BaseEntity)
            entity = cls(*args, **kwargs)
        self.entity_lst.append(entity)

    def remove(self, entity: BaseEntity):
        self.entity_lst.remove(entity)
