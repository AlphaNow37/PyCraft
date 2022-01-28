from .seeder import random
from ..constants import *
from .generation_blocks import BLOCKS, WATER_PATCHES_BLOCKS, FLEURS_BLOCKS_NAMES, COLORS_TERRACOTTA
from .BaseGenerator import BaseGenerator

AIR_BLOCKS = ["air", "snow"] + FLEURS_BLOCKS_NAMES


class TerrainGenerator(BaseGenerator):
    def __init__(self):
        super(TerrainGenerator, self).__init__()
        self.resume_world = []

        self.__y = HEIGHT_OCEAN
        self.__pente = 0
        self.__first = True
        self.tops = []

        self.__act_water_patch = BLOCKS[random.choice(WATER_PATCHES_BLOCKS)]
        self.__next_water_patch = random.randint(10, 15)

    def generate(self):
        super().generate()
        self.resume_world.append([BLOCKS["AIR"] for _ in range(HEIGHT_WORLD)])
        y = self.__y
        if not self.__first:
            self.__pente += random.choice(
                [-1, 0, 0, 1,
                 1 if self.__pente < 0 else 0 if self.__pente == 0 else -1,
                 1 if self.__pente < 0 else 0 if self.__pente == 0 else -1,
                 1 if y < HEIGHT_OCEAN + 5 else -1])
            if self.__pente >= 4:
                self.__pente = 3
            if self.__pente <= -4:
                self.__pente = -3
            if y >= 75:
                self.__pente -= 1
            if y <= 35:
                self.__pente += 1

            self.__y += self.__pente
            y = self.__y

        colonne = self.resume_world[-1]
        nb_dirts = random.randint(2, 3)
        colonne[:y - nb_dirts] = [BLOCKS["STONE"]] * (y - nb_dirts)

        if y < HEIGHT_OCEAN:
            self.__next_water_patch -= 1
            if self.__next_water_patch == 0:
                self.__act_water_patch = BLOCKS[random.choice(WATER_PATCHES_BLOCKS)]
                self.__next_water_patch = random.randint(10, 15)
            colonne[y - nb_dirts:y + 1] = [self.__act_water_patch] * (nb_dirts + 1)
            if self.height_snow == HEIGHT_OCEAN:
                nb_ice = min(random.randint(1, 3), HEIGHT_OCEAN-y)
                colonne[y + 1: HEIGHT_OCEAN] = [BLOCKS["WATER"]] * (HEIGHT_OCEAN - y - 1)
                colonne[HEIGHT_OCEAN-nb_ice+1:HEIGHT_OCEAN+1] = [BLOCKS["ICE"]]*nb_ice
            else:
                colonne[y + 1: HEIGHT_OCEAN + 1] = [BLOCKS["WATER"]] * (HEIGHT_OCEAN - y)
        else:
            if self.biome == "desert":
                colonne[y - nb_dirts:y+1] = [BLOCKS["SAND"]] * (nb_dirts + 1)
            elif self.biome == "mesa":
                colonne[y-nb_dirts-3:y+1] = [
                    BLOCKS[COLORS_TERRACOTTA[y_ % len(COLORS_TERRACOTTA)].upper()+"_TERRACOTTA"]
                    for y_ in range(y-nb_dirts-3, y+1)
                ]
            else:
                colonne[y - nb_dirts:y] = [BLOCKS["DIRT"]] * nb_dirts
                colonne[y] = BLOCKS["GRASS"]
            if y >= self.height_snow:
                colonne[y+1] = BLOCKS["SNOW"]
        self.tops.append(y)
        self.__first = False
        assert len(colonne) == HEIGHT_WORLD

    def remove_first_column(self):
        super().remove_first_column()
        del self.resume_world[0]
        del self.tops[0]

    def puts(self, to_put: list[dict]):
        x_ = 0
        while x_ < len(to_put):
            element = to_put[x_]
            element["x"] -= 1
            if element["x"] < 0:
                condition = element.get("condition", lambda *_, **__: True)
                is_ore = element.get("is_ore", False)
                x = element["x"]
                y = element["y"]
                block = element["block"]
                if condition(x, y) and 0 <= y < HEIGHT_WORLD:
                    if is_ore:
                        block[1]["name_fond"] = self.resume_world[x][y][0]
                    self.resume_world[x][y] = block
                del to_put[x_]
            else:
                x_ += 1

    def is_air(self, x, y):
        try:
            return self.resume_world[x][y][0] in AIR_BLOCKS
        except IndexError:
            return False
