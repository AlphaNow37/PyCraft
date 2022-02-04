from . import Block


class GravityBlock(Block):
    falling = False

    def update_from_voisin(self, from_x, from_y):
        if (from_x, from_y) == (0, -1):
            block = self.map.get_case(self.x, self.y-1)
            if block and block.air:
                self.map.set_case(self.x, self.y-1, self)
                self.map.destroy_case(self.x, self.y, particle=False)
                self.y -= 1
                self.falling = True
                self.map.to_planned_update.append([2, self.x, self.y])
            else:
                self.falling = False

    def planned_update(self):
        if self.falling:
            self.update_from_voisin(0, -1)
