from .. import container
from .. import items
from .. import Game


class PlayerInventory:
    def __init__(self, game):
        self.inventory = container.Container(36)
        self.hotbar = container.Container(9)
        self.upinventory = container.Container(27)
        self.hand_position = 0
        self.game: Game = game
        self.player = self.game.player

    def drop_item_or_stack(self, item_or_stack):
        if not isinstance(item_or_stack, container.Stack):
            item = items.item.get_item(item_or_stack)
            stack = container.Stack(item, 1)
        else:
            stack = item_or_stack
        item = items.dropped_item.DroppedItem(self.game, self.player.x, self.player.y,
                                              stack, self.player.vue_dir, time_cant_be_taked=50)
        self.game.entities.add(item)

    def take_item(self, item, count=1):
        item, count = container.get_item_and_count(item, count)
        for fillmode in (False, True):
            if count:
                count = self.hotbar.add_item(item, count, fillmode=fillmode)
            if count:
                count = self.upinventory.add_item(item, count, fillmode=fillmode)
        return count
