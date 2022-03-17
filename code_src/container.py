import pygame
from .items.item import Item, get_item
from .minecraft_font import get_surface_line


class Container:
    """Class to contain items"""
    def __init__(self, size, grid=None):
        if grid is None:
            grid = [None] * size
        self.grid: list[Stack | None] = grid
        self.size = size

    def add_item_at(self, position, item, count=1, _do_cast=True) -> int:
        if count <= 0:
            return 0
        if _do_cast:  # To add performance
            item, count = _get_item_and_count(item, count)
        stack = self.grid[position]
        if stack is None:
            self.grid[position] = stack = Stack(item, size=0)
            return stack.take(count)
        elif stack.item == item:
            return stack.take(count)
        return count

    def add_item(self, raw_item, count=1) -> int:
        """
        Add an item in the container
        :param raw_item: the item
        :param count: the item count
        :return: the numbers of unfilled items
        """
        item, count = _get_item_and_count(raw_item, count)
        for x, stack in enumerate(self.grid):
            count = self.add_item_at(x, item, count, _do_cast=False)
            if count <= 0:
                return 0
        return count

    def __repr__(self):
        return f"Cont(size={self.size} ...)"

    def __iter__(self):
        return iter(self.grid)

    def __len__(self):
        return self.size

    def __getitem__(self, item):
        if isinstance(item, int):
            return self.grid[item]
        elif isinstance(item, slice):
            return ContainerFragment(item, self)
        else:
            return NotImplemented

    def __setitem__(self, key, value):
        key = int(key)
        if value is not None:
            value = Stack.new(value)
        self.grid[key] = value

class Stack:
    """Represent an item with a quantity"""
    maxsize = 64

    @classmethod
    def new(cls, obj, count=1):
        if isinstance(obj, Stack):
            return obj
        else:
            return Stack(get_item(obj), count)

    def __init__(self, item, size=1):
        self.item: Item = item
        self.size = size

    def drop(self, number):
        if number > self.size:
            raise ValueError(number, self.size)
        self.size -= number

    def take(self, number) -> int:
        if self.maxsize < number + self.size:
            last_size = self.size
            self.size = self.maxsize
            return last_size + number - self.maxsize
        self.size += number
        return 0

    def is_full(self):
        return self.size <= self.maxsize

    def __repr__(self):
        return f"Stck(size={self.size},item={self.item})"

    def get_img(self):
        item_img: pygame.Surface = self.item.img
        item_surface = pygame.Surface((item_img.get_width()+3, item_img.get_height()))
        item_surface.fill("#123456")  # random color
        item_surface.set_colorkey("#123456")

        item_surface.blit(item_img, (0, 0))
        if self.size > 1:
            text = get_surface_line(f"{self.size:>2}")
            item_surface.blit(text, (item_img.get_width()-13, item_img.get_height()-8))
        # print((item_img.get_width()-4, item_img.get_height()-4), item_surface.get_size(), text.get_size())
        # pygame.show(item_surface)
        return item_surface

class ContainerFragment:
    """When you type container[slice]
    It is syncronized with the container"""
    def __init__(self, indexs: slice, superior: Container):
        self.grid = superior.grid
        indexs = slice(indexs.start or 0, indexs.stop or len(superior))
        self.size = indexs.stop - indexs.start
        self.indexs = indexs

    def __iter__(self):
        return iter(self.grid[self.indexs])

    def __repr__(self):
        return f"FragCont(size={self.size} indexs={self.indexs} ...)"

    def __len__(self):
        return self.size

    def __getitem__(self, item):
        return self.grid[self.indexs][item]

    def __setitem__(self, key, value):
        self.grid[self.indexs.start + key] = value


def _get_item_and_count(raw_item, raw_count=1) -> tuple[Item, int]:
    if isinstance(raw_item, Stack):
        count, item = raw_item.size, raw_item.item
    else:
        item: Item = get_item(raw_item)
        count = raw_count
    return item, count
