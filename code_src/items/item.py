from .loader import items
from ..blocks import blocks, Block

class Item:
    """A dataclass"""
    item_type = None
    damages = 1
    efficiency = 1
    solidity = None

    def __init__(self, name, image, **kwargs):
        self.name = name
        self.img = image
        self.__dict__.update(items.get(self.name, {}))
        self.__dict__.update(kwargs)

    def __eq__(self, other) -> bool:
        other_item = get_item(other)
        if other_item.name == self.name:
            return True
        return False


def get_item(item, **kwargs) -> Item:
    if isinstance(item, Item):
        return item
    elif isinstance(item, dict):
        return Item(**item, **kwargs)
    elif isinstance(item, (tuple, list)):
        return Item(*item, **kwargs)
    elif isinstance(item, str):
        return Item(item, blocks[item]["img"], **kwargs)
    elif isinstance(item, Block):
        return Item(item.name, item.img, **kwargs, item_type="block")
    else:
        raise ValueError(item)
