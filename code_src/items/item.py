
class Item:
    """A dataclass"""

    def __init__(self, name, image):
        self.name = name
        self.img = image


def get_item(item) -> Item:
    if isinstance(item, Item):
        return item
    elif isinstance(item, dict):
        return Item(**item)
    elif isinstance(item, (tuple, list)):
        return Item(*item)
    elif isinstance(item, str):
        pass
    else:
        raise ValueError(item)
