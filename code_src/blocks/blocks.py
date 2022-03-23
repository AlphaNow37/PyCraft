import pygame
from .. import base_elements
from . import loader
from .. import entity
from .. import Game
from ..items import dropped_item


class Block(base_elements.BaseCarre):
    """Classe mere de tous les blocks"""
    collision = True  # If the object has collision
    falling_max_speed = None  # For water / ladders / ...

    air = False  # For air only
    unbreakable = False  # Bedrock, water, ...
    revelated = True  # For Ores
    solidity = 0.5  # For the mining speed
    outil = None  # "pickaxe" -> stone, etc

    drop_value = None  # None -> himself, dict[str, int] -> int instances of str item
                       # dict[str, dict[...]] -> custom 0->nothing
                       # str -> the block with name=str

    support_x_flip = False  # If we can flip vertically
    support_y_flip = False  # ~ horizontally

    is_slab = False

    destroyed = False  # never True beetween 2 ticks

    breaked_sound = None  # The name of his breaked-sound

    @staticmethod
    def func_get_pos_friends(_x, _y): return []

    def __init__(self, name, game: Game, x, y, **kwargs):
        super().__init__(game, x, y)
        self.name = name
        self.__dict__.update(blocks[name])
        self.__dict__.update(kwargs)
        self.img.set_colorkey((0, 0, 0, 0))
        if self.is_slab:
            self.draw = self.slab_draw
        self.friends: list[tuple[int, int]] = self.func_get_pos_friends(self.x, self.y)

    def __repr__(self):
        return f"{self.__class__.__name__}('{self.name}',x={self.x}, y={self.y})"

    def revelate(self):
        if not self.revelated:
            self.revelated = True
            for case in self.map.get_around(self.x, self.y):
                case.revelate()

    def destroy(self, particle=True, sound=True, do_drop=False):
        self.destroyed = True
        for friend in self.friends:
            case = self.map.get_case(*friend)
            if case and not case.destroyed:
                self.map.destroy_case(*friend, sound=False, do_drop=True)
        if particle:
            for _ in range(5):
                self.game.entities.add(entity.Particle(self.game, self.x + 0.5, self.y + 0.5, self.img))
        if sound:
            self.game.sound_manager.breaked(self.breaked_sound)
        if do_drop:
            self.drop()

    def update_from_voisin(self, from_x, from_y):
        pass

    def planned_update(self):
        pass

    def drop(self):
        to_drop = []
        is_block = False
        if self.drop_value is None:
            to_drop = [(self.name, self.img)]
            is_block = True
        elif isinstance(self.drop_value, str):
            to_drop = [self.drop_value]
            is_block = True
        for item in to_drop:
            item = dropped_item.DroppedItem(self.game, self.x+0.5, self.y+0.5, item, isblock=is_block)
            self.game.entities.add(item)

    def slab_draw(self, x_self=None, y_self=None, img=None, width=None, height=None, frame=None):
        y_self = y_self if y_self is not None else self.y
        super().draw(x_self, y_self+0.5-0.5*self.flip_y, img, width, height, frame)

    def get_visualisation(self):
        return {
            name: value
            for name in ("air", "collision", "unbreakable", "outil", "name_fond", "flip_x", "flip_y")
            if (value := getattr(self, name, None)) != getattr(Block, name, None)
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
