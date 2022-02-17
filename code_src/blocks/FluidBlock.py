from . import Block


class FluidBlock(Block):
    """Classe de tous les fluides"""
    fluidity = 3  # for water

    def update_from_voisin(self, from_x, from_y):
        if from_y == 1:
            return
        x = self.x+from_x
        y = self.y+from_y
        block = self.map.get_case(x, y)
        if block and block.air:
            self.map.set_case(x, y, FluidBlock("water", self.game, x, y))
            self.map.to_planned_update.append([self.fluidity, x, y])

    def planned_update(self):
        for x_, y_ in [(-1, 0), (1, 0), (0, 1), (0, -1)]:
            self.update_from_voisin(x_, y_)
