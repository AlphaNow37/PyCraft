from . import Block
from .. import entity


class GravityBlock(Block):
    def update(self, from_x, from_y):
        if (from_x, from_y) == (0, -1):
            block = self.map.get_case(self.x, self.y-1)
            if block and block.air:
                self.map.destroy_case(self.x, self.y)
                self.game.entity_manager.add(entity.FallingBloockEntity(self.game, self.x, self.y-1, self))
