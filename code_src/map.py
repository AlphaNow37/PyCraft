import json

from .player import Player
from . import blocks
from .generation import Generator, load_from_data, get_data_from_gen, seeder
from .constants import *

"""
Fichier servant a gérer la map, et déclanchant les générations de terrain

resume :
-> ("name", {"propname": <value>})
-> est une version simplifiée du block
"""


dct_name_to_cls = {
    "ORE": blocks.Ore,
    "GRASS": blocks.Grass,
    "BIG_FLOWER_UP": blocks.BigFlowerUp,
    "BIG_FLOWER_BOTTOM": blocks.BigFlowerBottom,
    "SUPPORTED_BLOCK": blocks.SupportedBlock,
    "GRAVITY": blocks.GravityBlock,
    "FLUID": blocks.FluidBlock,
}
dct_cls_to_name = {
    cls: name for (name, cls) in dct_name_to_cls.items()
}


class Map:
    to_planned_update: list[list[int]]

    def __init__(self, game):
        self.game = game

    def generate(self):
        """
        Cette méthode crée la map, place le joueur et commence la génération
        """
        self.to_planned_update: list[list[int, int, int]] = []

        self.left_generator = Generator()
        self.left_generator.setup()
        self.left_world: list[list[blocks.Block]] = []
        self.left_biomes = []

        self.right_generator = Generator()
        self.right_generator.setup()
        self.right_world: list[list[blocks.Block]] = []
        self.right_biomes = []

        self.player = Player(self.game, self.get_top(0) + 0.5)

        self.seed = seeder.seeder.seed

    def tick(self):
        i = 0
        while i < len(self.to_planned_update):
            nb_ticks, x, y = self.to_planned_update[i]
            nb_ticks -= 1
            if nb_ticks == 0:
                self.get_case(x, y).planned_update()
                del self.to_planned_update[i]
            else:
                self.to_planned_update[i][0] = nb_ticks
                i += 1

    def draw(self):
        """
        affiche tout les blocks
        """
        x_cam, y_cam = map(int, self.game.camera_center)
        zoom = self.game.zoom
        for x in range(x_cam-zoom-1, x_cam+zoom+1):
            for y in range(y_cam - zoom - 1, y_cam + zoom + 1):
                block = self.get_case(x, y)
                if block is not None and not block.air:
                    block.draw()

    def get_case(self, x, y) -> blocks.Block | None:
        """
        retourne le Block situé en (x; y) si existant
        """
        x = int(x)
        y = int(y)
        if not 0 <= y < HEIGHT_WORLD:
            return None
        x_, world, side = self._get_world_from_x(x)
        if x_+20 > len(world):
            for _ in range(x_ - len(world) + 1):
                self._add_column(side)
        return world[x_][y]

    def get_top(self, x):
        for y in range(HEIGHT_WORLD):
            case = self.get_case(x, y)
            if case is not None and case.air:
                return y

    def get_block_from_resume(self, resume, x, y, is_left=False) -> blocks.Block:
        name, properties = resume
        if name == "forced_air":
            name = "air"
        properties: dict = properties.copy()
        if is_left and "flip_x" in properties:
            properties["flip_x"] = not properties["flip_x"]
        cls: type[blocks.Block] = properties.pop("class", None)
        if isinstance(cls, str):
            cls = dct_name_to_cls[cls]
        elif cls is None:
            cls = blocks.Block
        block = cls(name, self.game, x, y, **properties)
        return block

    def _add_column(self, side, column=None):
        world = self.left_world if side == -1 else self.right_world
        transformer_x = (lambda x: -x-1) if side == -1 else (lambda x: x)
        li_biome = self.left_biomes if side == -1 else self.right_biomes
        if column is None:
            generator = self.left_generator if side == -1 else self.right_generator
            generator.generate()
            world.append(
                [self.get_block_from_resume(resume, transformer_x(len(world)), y, side == -1)
                 for y, resume in enumerate(generator.resume_world[0])]
            )
            li_biome.append(generator.biomes[0])
            generator.remove_first_column()
        else:
            world.append(
                [self.get_block_from_resume(resume, transformer_x(len(world)), y)
                 for y, resume in enumerate(column)]
            )

    def _get_world_from_x(self, x):
        return (abs(x)-1, self.left_world, -1) if x < 0 else (x, self.right_world, 1)

    def get_biome(self, x=None):
        if x is None:
            x = self.game.player.x
        x, _, side = self._get_world_from_x(x)
        li_biome = self.left_biomes if side == -1 else self.right_biomes
        return li_biome[int(x)]

    def destroy_case(self, x, y, particle=True, sound=True):
        """
        détruit le block en (x; y)
        :param particle: si la destruction emet des particules
        """
        new_x, world, _ = self._get_world_from_x(x)
        self.get_case(x, y).destroy(particle=particle, sound=sound)
        world[new_x][y] = blocks.Block("air", self.game, new_x, y)
        self.update_around(x, y)
        for case in self.get_around(x, y):
            case.revelate()

    def update_around(self, x, y):
        """
        update tous les voisins de (x; y)
        """
        for x_, y_ in [(0, 1), (1, 0), (-1, 0), (0, -1)]:
            case = self.get_case(x+x_, y+y_)
            if case is not None:
                case.update_from_voisin(-x_, -y_)

    def get_around(self, x, y) -> list[blocks.Block]:
        cases = []
        for x_, y_ in [(0, 1), (1, 0), (-1, 0), (0, -1)]:
            case = self.get_case(x+x_, y+y_)
            if case is not None:
                cases.append(case)
        return cases

    def set_case(self, x, y, *args, **kwargs):
        """
        Place un block
        :param x: la position du block en x
        :param y: la position du block en y
        :param args, kwargs: (<block>,) {} -> place directement le block
                            sinon place kwargs.pop("cls", Block)(*args, **kwargs)
        """
        x = int(x)
        y = int(y)
        if len(args) == 1 and not kwargs and isinstance(args[0], blocks.Block):
            block: blocks.Block = args[0]
        else:
            cls = kwargs.pop("cls", blocks.Block)
            block: blocks.Block = cls(*args, **kwargs)
        x_, world, side = self._get_world_from_x(x)
        if x_+20 > len(world):
            for _ in range(x_ - len(world) + 1):
                self._add_column(side)
        world[x_][y] = block

    def get_world_data(self):
        """
        :return: les data du monde (le monde de gauche, celui de droite, idem pr les biomes)
        """
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
            } | {
                "left_biomes": self.left_biomes,
                "right_biomes": self.right_biomes,
            }
        )

    def set_world_data(self, data: dict[str, list[list[tuple[str, dict[str, str]]]]]):
        self.left_world = []
        self.right_world = []
        self.left_biomes = data["left_biomes"]
        self.right_biomes = data["right_biomes"]
        for name, side in (("left", -1), ("right", 1)):
            for column in data[name]:
                self._add_column(side, column)

    def get_little_data(self):
        """
        retourne les données relatives aux générateur et au joueur
        :return: dict
        """
        return {
            "left_gen": get_data_from_gen(self.left_generator),
            "right_gen": get_data_from_gen(self.right_generator),
            "player": self.player.get_data(),
            "seed": self.seed,
        }

    def set_little_data(self, data):
        seeder.seeder.reset(data["seed"])
        self.left_generator = load_from_data(data["left_gen"])
        self.right_generator = load_from_data(data["right_gen"])
        self.player.set_data(data["player"])
