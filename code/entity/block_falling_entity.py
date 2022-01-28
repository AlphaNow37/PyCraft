from . import base_entity
from .. import blocks


class FallingBloockEntity(base_entity.BaseEntity):
    fall = True
    width = 0.3
    height = 0.3

    def __init__(self, game, x, y, block_replace: blocks.Block, **kwargs):
        super().__init__(game, x, y, **kwargs)
        self.img = block_replace.img
        self.block_replace = block_replace

    def tick(self):
        super().tick()
        if self.act_speed_y == 0:  # Stop falling
            self.block_replace.x = int(self.x)
            self.block_replace.y = int(self.y)
            self.map.destroy_case(int(self.x), int(self.y))
            self.map.set_case(int(self.x), int(self.y), self.block_replace)
            self.destroy()
