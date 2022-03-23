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

    def get_main_hand_item(self) -> "items.item.Item | None":
        stack = self.hotbar[self.hand_position]
        return stack if stack is None else stack.item

    def get_mining_speed(self, name_outil):
        if self.game.is_admin:
            return float("inf")
        in_main = self.get_main_hand_item()
        if name_outil is None or in_main is None:
            return 1
        else:
            if name_outil == in_main.item_type:
                return in_main.efficiency
            else:
                return 1
