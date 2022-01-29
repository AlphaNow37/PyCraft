import pygame
from .. import base_elements
from . import loader
from .. import entity


class Block(base_elements.BaseCarre):
    collision = True
    air = False
    unbreakable = False
    revelated = False
    solidity = 0.5
    outil = None

    destroyed = False

    @staticmethod
    def func_get_pos_friends(_x, _y): return []

    def __init__(self, name, game, x, y, **kwargs):
        super().__init__(game, x, y)
        self.name = name
        self.__dict__.update(blocks[name])
        self.__dict__.update(kwargs)
        self.img.set_colorkey((0, 0, 0, 0))

        self.friends: list[tuple[int, int]] = self.func_get_pos_friends(self.x, self.y)

    def __repr__(self):
        return f"{self.__class__.__name__}('{self.name}',x={self.x}, y={self.y})"

    def revelate(self):
        if self.air and not self.revelated:
            for x, y in [(0, 1), (1, 0), (-1, 0), (0, -1)]:
                x += self.x
                y += self.y
                block = self.map.get_case(x, y)
                if block is not None and not block.revelated:
                    block.revelate()
        self.revelated = True

    def destroy(self):
        self.destroyed = True
        for friend in self.friends:
            case = self.map.get_case(*friend)
            if case and not case.destroyed:
                self.map.destroy_case(*friend)
        for _ in range(5):
            self.game.entity_manager.add(entity.Particle(self.game, self.x+0.5, self.y+0.5, self.img))

    def update(self, from_x, from_y):
        pass

    def get_visualisation(self):
        return {
            name: value
            for name in ("air", "collision", "unbreakable", "outil")
            if (value := getattr(self, name)) != getattr(Block, name)
        } | {
            name: value
            for name in ("solidity", )
            if (value := getattr(self, name)) is not None
        }

    def get_reduced_visualisation(self):
        return {
            name: value
            for (name, value) in self.get_visualisation().items()
            if blocks[self.name].get(name, ...) != value
        }

    def as_str_vue(self, visu=None):
        visu = visu if visu is not None else self.get_visualisation()
        _n = "\n"
        return f"""
Name: {self.name}
Pos:
    X: {self.x} Y: {self.y}
Class: {self.__class__.__name__}
{_n.join(f'{name.title()}: {value}' for name, value in visu.items())}
""".strip()


def get_surface_color(color):
    surface = pygame.Surface((1, 1))
    surface.fill(color)
    return surface


def get_rectangle(height, total_height, color):
    surface = pygame.Surface((1, height))
    surface.fill(color)
    total_surface = pygame.Surface((1, total_height))
    total_surface.blit(surface, (0, total_height - height))
    return total_surface


blocks = loader.blocks
