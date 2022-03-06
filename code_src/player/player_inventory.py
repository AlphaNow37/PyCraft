from .. import container


class PlayerInventory:
    def __init__(self):
        self.inventory = container.Container(2)
        self.take_item = self.inventory.add_item
        self.hand_position = 0
