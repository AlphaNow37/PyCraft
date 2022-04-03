from . import Block


class SupportedBlock(Block):
    """Classe de tous les blocks supportés par un autre block"""
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
                    self.map.destroy_case(self.x, self.y, do_drop=True)

    @classmethod
    def place_at(cls, name, game, x, y, **kwargs):
        block = super().place_at(name, game, x, y, **kwargs)
        block.update_from_voisin(block.support_from_x, block.support_from_y)
        return block


def partial_cls(name, cls_base, **kwargs):
    return type(name, (cls_base,), kwargs)

BigFlowerBottom = partial_cls(
    "BigFlowerBottom", SupportedBlock,
    func_get_pos_friends=lambda _, x, y: [(x, y+1)])

class BigFlowerUp(Block):
    @staticmethod
    def func_get_pos_friends(x, y):
        return [(x, y-1)]

    @classmethod
    def place_at(cls, name: str, game, x, y, **kwargs):
        if game.map.get_case(x, y+1) is None or not game.map.get_case(x, y+1).air:
            return False
        b2 = super().place_at(name, game, x, y + 1)
        BigFlowerBottom.place_at(name.removesuffix("_1")+"_0", game, x, y)
        return b2
