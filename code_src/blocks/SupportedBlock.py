from . import Block
from functools import partial


class SupportedBlock(Block):
    def __init__(self, name, game, x, y, support_from=(0, -1), **kwargs):
        super().__init__(name, game, x, y, **kwargs)
        self.support_from_x, self.support_from_y = self.support_from = support_from

    def update_from_voisin(self, from_x, from_y):
        if self.destroyed:
            return
        if (from_x, from_y) == self.support_from:
            case = self.map.get_case(self.x+self.support_from_x, self.y+self.support_from_y)
            if isinstance(case, Block):
                if case.air or not case.collision:
                    self.map.destroy_case(self.x, self.y)


BigFlowerUp = partial(Block, func_get_pos_friends=lambda x, y: [(x, y-1)])
BigFlowerBottom = partial(SupportedBlock, func_get_pos_friends=lambda x, y: [(x, y+1)])
