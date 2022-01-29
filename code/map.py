import json
from .player import Player
from . import blocks
from typing import Union
from .generation import Generator
from .constants import *

"""
Fichier servant a gérer la map, et déclanchant les générations de terrain
"""


dct_name_to_cls = {
                "ORE": blocks.Ore,
                "GRASS": blocks.Grass,
                "BIG_FLOWER_UP": blocks.BigFlowerUp,
                "BIG_FLOWER_BOTTOM": blocks.BigFlowerBottom,
                "SUPPORTED_BLOCK": blocks.SupportedBlock,
                "GRAVITY": blocks.GravityBlock,
            }
dct_cls_to_name = {
    cls: name for (name, cls) in dct_name_to_cls.items()
}


class Map:
    def __init__(self, game):
        self.game = game

    def generate(self):
        self.left_generator = Generator()
        self.left_generator.setup()
        self.left_world = []
        self.left_biomes = []

        self.right_generator = Generator()
        self.right_generator.setup()
        self.right_world: list[list[blocks.Block]] = []
        self.right_biome: list[list[blocks.Block]] = []

        self.player = Player(self.game, self.get_top(0) + 0.5)

    def draw(self):
        x_cam, y_cam = map(int, self.game.camera_center)
        zoom = self.game.zoom
        for x in range(x_cam-zoom-1, x_cam+zoom+1):
            for y in range(y_cam - zoom - 1, y_cam + zoom + 1):
                block = self.get_case(x, y)
                if block is not None and not block.air:
                    block.draw()

    def get_case(self, x, y) -> Union[blocks.Block, None]:
        x = int(x)
        y = int(y)
        if not 0 <= y < HEIGHT_WORLD:
            return None
        x_, world, cote = self._get_world_from_x(x)
        if x_+20 > len(world):
            for _ in range(x_ - len(world) + 1):
                self._add_column(cote)
        return world[x_][y]

    def get_top(self, x):
        for y in range(HEIGHT_WORLD):
            case = self.get_case(x, y)
            if case is not None and case.air:
                return y

    def get_block_from_resume(self, resume, x, y) -> blocks.Block:
        name, properties = resume
        properties = properties.copy()
        properties: dict
        classe: type[blocks.Block] = properties.pop("class", None)
        if isinstance(classe, str):
            classe = dct_name_to_cls[classe]
        elif classe is None:
            classe = blocks.Block
        block = classe(name, self.game, x, y, **properties)
        return block

    def _add_column(self, cote):
        generator = self.left_generator if cote == -1 else self.right_generator
        generator.generate()
        world = self.left_world if cote == -1 else self.right_world
        transformer_x = (lambda x: -x-1) if cote == -1 else (lambda x: x)
        li_biome = self.left_biomes if cote == -1 else self.right_biome
        world.append(
            [self.get_block_from_resume(resume, transformer_x(len(world)), y)
             for y, resume in enumerate(generator.resume_world[0])]
        )
        li_biome.append(generator.biomes[0])
        generator.remove_first_column()

    def _get_world_from_x(self, x):
        return (abs(x)-1, self.left_world, -1) if x < 0 else (x, self.right_world, 1)

    def get_biome(self, x=None):
        if x is None:
            x = self.game.player.x
        x, _, cote = self._get_world_from_x(x)
        li_biome = self.left_biomes if cote == -1 else self.right_biome
        return li_biome[int(x)]

    def destroy_case(self, x, y):
        new_x, world, _ = self._get_world_from_x(x)
        self.get_case(x, y).destroy()
        world[new_x][y] = blocks.Block("air", self.game, new_x, y)
        self.update_around(x, y)

    def update_around(self, x, y):
        for x_, y_ in [(0, 1), (1, 0), (-1, 0), (0, -1)]:
            case = self.get_case(x+x_, y+y_)
            if isinstance(case, blocks.Block):
                case.update(-x_, -y_)

    def get_around(self, x, y) -> list[blocks.Block]:
        cases = []
        for x_, y_ in [(0, 1), (1, 0), (-1, 0), (0, -1)]:
            case = self.get_case(x+x_, y+y_)
            if isinstance(case, blocks.Block):
                cases.append(case)
        return cases

    def set_case(self, x, y, *args, **kwargs):
        x = int(x)
        y = int(y)
        if len(args) == 1 and not kwargs and isinstance(args[0], blocks.Block):
            block: blocks.Block = args[0]
        else:
            cls = kwargs.pop("cls", blocks.Block)
            block: blocks.Block = cls(*args, **kwargs)
        x_, world, cote = self._get_world_from_x(x)
        if x_+20 > len(world):
            for _ in range(x_ - len(world) + 1):
                self._add_column(cote)
        world[x_][y] = block

    def get_world_data(self):
        return json.dumps(
            {
                name: [
                    [
                        [
                            case.name,
                            case.get_reduced_visualisation()
                            | ({"class": dct_cls_to_name[case.__class__]} if case.__class__ != blocks.Block else {})
                        ] for case in column
                    ] for column in world
                ] for (name, world) in [("left", self.left_world), ("right", self.right_world)]
            }
        )
