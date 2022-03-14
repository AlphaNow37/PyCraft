import pygame
from .items.item import Item, get_item
from .minecraft_font import get_surface_line


class Container:
    def __init__(self, size, grid=None):
        if grid is None:
            grid = [None] * size
        self.grid: list[Stack | None] = grid
        self.size = size

    def set_at(self, x, raw_stack):
        stack = Stack.new(raw_stack)
        self.grid[x] = stack

    def get_at(self, x) -> "Stack | None":
        return self.grid[x]

    def add_item(self, raw_item, count=1):
        if isinstance(raw_item, Stack):
            count, item = raw_item.size, raw_item.item
        else:
            item: Item = get_item(raw_item)
        for x, stack in enumerate(self.grid):
            if stack is None:
                stack_size = min(64, count)
                self.grid[x] = Stack(item, stack_size)
                count -= stack_size
            elif stack.item.name == item.name:
                stack_size = min(64-stack.size, count)
                stack.take(stack_size)
                count -= stack_size
            if count == 0:
                return True
        return False

    def __repr__(self):
        return f"Cont(size={self.size} ...)"

    def __iter__(self):
        return iter(self.grid)

    def __len__(self):
        return self.size

    def __getitem__(self, item):
        return self.grid[item]

class Stack:
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

    def take(self, number):
        if self.maxsize < number + self.size:
            raise ValueError(number, self.size)
        self.size += number

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
import csv