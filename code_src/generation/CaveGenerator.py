from .generation_blocks import BLOCKS, STONES
from .TerrainGenerator import TerrainGenerator
from .seeder import random
from ..constants import *
from dataclasses import dataclass


CAVE_REPLACABLE = STONES+["DIRT", "SAND", "GRAVEL", "GRASS"]


class CaveGenerator(TerrainGenerator):
    def __init__(self):
        super().__init__()
        self.__caves: list[Cave] = []

    def generate(self):
        super().generate()
        if len(self.tops) > 4:
            if 5 < len(self.tops) < 7:
                self.add_cave()
            x_ = 0
            while x_ < len(self.__caves):
                cave = self.__caves[x_]
                cave.height += random.choice([
                    0, 1, -1,
                    -1 if cave.height > 3 else 0,
                    1 if cave.height < 2 else 0,
                ])
                if cave.height == 0:
                    self.__caves.remove(cave)
                    self.add_cave()
                    continue

                cave.direction += random.choice([
                    1, -1,
                    -1 if cave.direction >= 1 else 0,
                    1 if cave.direction <= -1 else 0,
                ])
                cave.direction = min(max(cave.direction, -1), 1)

                cave.y += cave.direction
                cave.y = min(max(cave.y, 4), HEIGHT_WORLD-cave.height-2)

                for y in range(cave.y, cave.y+cave.height):
                    if self.resume_world[-1][y][0].upper() in CAVE_REPLACABLE:
                        self.resume_world[-1][y] = BLOCKS["AIR"]

                x_ += 1

    def add_cave(self):
        self.__caves.append(Cave(
            random.randint(6, HEIGHT_WORLD),
            random.randint(1, 2),
            random.randint(-1, 1)))


@dataclass
class Cave:
    y: int
    height: int
    direction: int
