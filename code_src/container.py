from .items.item import Item, get_item


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
