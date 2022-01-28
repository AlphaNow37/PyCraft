from .seeder import random
import math

from .PatchGenerator import PatchGenerator
from ..constants import *
from .generation_blocks import BLOCKS, FLEURS_NAMES


class VegetationGenerator(PatchGenerator):
    def __init__(self):
        super().__init__()
        self.__next_tree = 7
        self.__next_minitree = 6
        self.__next_small_area = 1  # <0 -> placing block; >0 -> waiting
        self.__to_put = []

    def generate(self):
        super().generate()
        self.puts(self.__to_put)
        self.__next_tree -= 1
        self.__next_minitree -= 1
        if self.__next_small_area > 0:
            self.__next_small_area -= 1
            if self.__next_small_area == 0:
                self.__next_small_area = random.randint(-10, -2)
        elif self.__next_small_area < 0:
            self.__next_small_area += 1
            if self.__next_small_area == 0:
                self.__next_small_area = random.randint(5, 15)
            y = self.tops[-2]
            if y > HEIGHT_OCEAN:
                if self.biome in ["plain", "birch_forest"] and self.is_air(-2, y+1):
                    fleur = random.choice(FLEURS_NAMES)
                    for h, name_morceau in enumerate(fleur):
                        block = BLOCKS[f"FLEUR_{name_morceau.upper()}"]
                        self.resume_world[-2][y+h+1] = block
                    return
        if len(self.tops) > 2:
            x_base = -2
            y_base = self.tops[-2] + 1
            name_struct = None
            if self.__next_tree <= 0:
                self.__next_tree = random.randint(3, 7)
                if self.tops[-2] > HEIGHT_OCEAN:
                    is_not_trou = self.tops[-3] <= self.tops[-2]+2 >= self.tops[-1]
                    if self.biome == "desert" and self.tops[-3] <= self.tops[-2] >= self.tops[-1]:
                        name_struct = "cactus"
                    elif (self.biome == "oak_forest" and is_not_trou
                            and self.__is_grass(-2)):
                        name_struct = "oak_tree"
                    elif (self.biome == "birch_forest" and is_not_trou
                            and self.__is_grass(-2)):
                        if random.randint(0, 5) == 0:
                            name_struct = "oak_tree"
                        else:
                            name_struct = "birch_tree"
                    elif (self.biome == "ice_peaks" and HEIGHT_OCEAN+3 < self.tops[-2]
                          and self.tops[-3] <= self.tops[-2]+2 >= self.tops[-1]):
                        name_struct = "ice_peak"
                    elif (self.biome == "spruce_forest" and is_not_trou
                            and self.__is_grass(-2)):
                        name_struct = "spruce_tree"
                    elif self.biome == "savan":
                        name_struct = "acacia_tree"
                        self.__next_tree += 15
            elif self.__next_minitree <= 0:
                self.__next_minitree = random.randint(3, 5)
                if self.tops[-2] > HEIGHT_OCEAN:
                    if self.biome == "desert":
                        if self.is_air(-2, self.tops[-2]+1):
                            self.resume_world[-2][self.tops[-2]+1] = BLOCKS["DEAD_BUSH"]
                            return
                    elif(self.biome == "jungle" and self.__is_grass(-2)
                            and self.__is_grass(-3) and self.tops[-2] <= 75):
                        name_struct = "jungle_tree"
            if name_struct is not None:
                for x_inc, y_inc, block, no_leaves in random.choice(structures[name_struct]):
                    x = x_base + x_inc
                    y = y_base + y_inc
                    if x < 0 and (self.is_air(x, y) or (no_leaves and self.__is_leaves_or_air(x, y))):
                        self.resume_world[x][y] = block
                    else:
                        self.__to_put.append({
                            "x": x,
                            "y": y,
                            "block": block,
                            "condition": self.__is_leaves_or_air if no_leaves else self.is_air
                        })

                return

    def __is_grass(self, x):
        return self.resume_world[x][self.tops[x]][0] == "grass"

    def __is_leaves_or_air(self, x, y):
        if self.is_air(x, y):
            return True
        try:
            return self.resume_world[x][y][0].endswith("leaves")
        except IndexError:
            return False


def get_structure(name, seed):
    if name == "cactus":
        return [(0, y, BLOCKS["CACTUS"], True) for y in range(seed+1)]

    elif name in ("oak_tree", "birch_tree"):
        name_tree = name.removesuffix("_tree").upper()
        height = seed+3
        return [
            (0, y, BLOCKS[f"{name_tree}_LOG"], True) for y in range(height)
        ] + [
            (x, y, BLOCKS[f"{name_tree}_LEAVES"], False)
            for x in range(-2, 3)
            for y in range(height, height+2 if abs(x) == 2 else height+3)
        ]
    elif name == "jungle_tree":
        height = seed+7
        coef_pente = 1.2
        height_leaves = 5
        max_width = int(coef_pente*height_leaves+1)
        return [
            (x, y, BLOCKS["JUNGLE_LOG"], True)
            for x in range(2)
            for y in range(-5, height)
        ] + [
            (x, y+height, BLOCKS["JUNGLE_LEAVES"], False)
            for y in range(height_leaves)
            for x in range(-max_width, max_width+3)
            if math.sqrt((x-0.5)**2+(y+1.4)**2) < max_width*0.75
        ]

    elif name == "spruce_tree":
        height = seed+2
        tree = [
            (0, y, BLOCKS["SPRUCE_LOG"], True)
            for y in range(height)
        ] + [
            (x, height+(max_width_plateau-y)+3*(3-max_width_plateau), BLOCKS["SPRUCE_LEAVES"], False)
            for max_width_plateau in range(1, 4)
            for y in range(max_width_plateau+1)
            for x in range(-y, y+1)
        ]
        return tree + [
            (x, y+1, BLOCKS["SNOW"], False)
            for x, y, _, _ in tree
        ]

    elif name == "acacia_tree":
        height = 3+(seed//2)
        first_bas = (seed % 2)*2-1
        size_branch = 3
        tree = [
            (0, y, BLOCKS["ACACIA_LOG"], True)
            for y in range(height)
        ]
        leaves_struct = [
            (x, y)
            for x in range(-3, 4)
            for y in range(1 if abs(x) == 3 else 2)
        ]
        for cote, dir_ in ((first_bas, 1), (-first_bas, 2)):
            tree += [
                (x*cote, height+(x*dir_)-1-h, BLOCKS["ACACIA_LOG"], True)
                for x in range(1, size_branch+1)
                for h in range(dir_)
            ] + [
                ((x+size_branch)*cote, height+y_+size_branch*dir_, BLOCKS["ACACIA_LEAVES"], False)
                for x, y_ in leaves_struct
            ]

        return tree

    elif name == "ice_peak":
        height = seed + 10
        return [
            (x, height-y-10, BLOCKS["ICE"], False)
            for y in range(height)
            for x in range(-(y//3), y//3+1)
        ] + [
            (x, -y-10, BLOCKS["ICE"], False)
            for y in range(10)
            for x in range(-((height-1)//3), (height-1)//3+1)
        ]

    else:
        raise ValueError(name)


def filter_structure(structure):
    filtered_structure = []
    xy_already_seen = set()
    for x, y, *other in structure:
        if (x, y) not in xy_already_seen:
            xy_already_seen.add((x, y))
            filtered_structure.append((x, y, *other))
    return filtered_structure


structures = {
    name: [filter_structure(get_structure(name, seed)) for seed in range(nb_seeds)]
    for name, nb_seeds in [
        ("oak_tree", 2),
        ("birch_tree", 2),
        ("jungle_tree", 13),
        ("spruce_tree", 2),
        ("acacia_tree", 10),
        ("cactus", 3),
        ("ice_peak", 10),
    ]
}
