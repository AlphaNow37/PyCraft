from .loader import items
from ..blocks import blocks

class Item:
    """A dataclass"""
    is_pickaxe = is_axe = is_sword = is_hoe = False
    is_boot = is_legs = is_chetplate = is_helmet = False
    damages = 1
    efficiency = 1
    solidity = None
    is_block = False

    def __init__(self, name, image, **kwargs):
        self.name = name
        self.img = image
        self.__dict__.update(items.get(self.name, {}))
        self.__dict__.update(kwargs)


def get_item(item) -> Item:
    if isinstance(item, Item):
        return item
    elif isinstance(item, dict):
        return Item(**item)
    elif isinstance(item, (tuple, list)):
        return Item(*item)
    elif isinstance(item, str):
        return Item(item, blocks[item]["img"], is_block=True)
    else:
        raise ValueError(item)
