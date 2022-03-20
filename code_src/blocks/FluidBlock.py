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
            self.map.set_case(x, y, FluidBlock(self.name, self.game, x, y))
            self.map.to_planned_update.append([int(10/self.fluidity), x, y])

    def planned_update(self):
        for x_, y_ in [(-1, 0), (1, 0), (0, 1), (0, -1)]:
            self.update_from_voisin(x_, y_)

    def draw(self, x_self=None, y_self=None, img=None, width=None, height=None, frame=None):
        superior = self.map.get_case(self.x, self.y+1)
        if isinstance(superior, FluidBlock):
            super(FluidBlock, self).draw(x_self, y_self, img, width, 1, frame)
        else:
            super(FluidBlock, self).draw(x_self, y_self, img, width, 0.9, frame)
