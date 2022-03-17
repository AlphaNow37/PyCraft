from .. import container
from .. import items
from .. import Game


class PlayerInventory:
    def __init__(self, game):
        self.inventory = container.Container(36)
        self.take_item = self.inventory.add_item
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
