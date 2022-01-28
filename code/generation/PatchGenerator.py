from .TerrainGenerator import TerrainGenerator
from .seeder import random
from .generation_blocks import BLOCKS, STONES
from ..constants import *

PATCHS = {
    patch[0]: {
        "block": BLOCKS[patch[0]],
        "min_y": patch[1], "max_y": patch[2],
        "min_blob_size": patch[3], "max_blob_size": patch[4],
        "frequency": 360//patch[5],
        "is_ore": patch[6],
    }
    for patch in [
        # NAME | min_y | max_y | MinBS | MaxBS | freq | is_ore
        ("GRANITE", 2, HEIGHT_OCEAN, 10, 15, 60, False),
        ("ANDESITE", 10, HEIGHT_WORLD//1.5, 10, 15, 60, False),
        ("DIORITE", 20, HEIGHT_WORLD-5, 10, 15, 60, False),

        ("DIRT", 2, HEIGHT_WORLD-5, 10, 15, 40, False),
        ("GRAVEL", 2, HEIGHT_WORLD-5, 10, 15, 40, False),

        ("IRON_ORE", 2, HEIGHT_WORLD-5, 4, 8, 60, True),
        ("COAL_ORE", 2, HEIGHT_WORLD-5, 4, 8, 120, True),
        ("GOLD_ORE", 2, round(HEIGHT_OCEAN/1.5), 4, 7, 30, True),
        ("EMERALD_ORE", 5, HEIGHT_OCEAN//3, 1, 2, 5, True),
        ("DIAMOND_ORE", 2, HEIGHT_OCEAN//4, 3, 6, 15, True),
    ]}


class PatchGenerator(TerrainGenerator):
    def __init__(self):
        super().__init__()

        self.nexts_patchs = {
            name: random.randint(2, properties["frequency"]*2)
            for name, properties in PATCHS.items()
        }
        self.__to_put = []

    def generate(self):
        super().generate()
        self.puts(self.__to_put)
        for name in self.nexts_patchs:
            self.nexts_patchs[name] -= 1
            if self.nexts_patchs[name] == 0:
                properties = PATCHS[name]
                self.nexts_patchs[name] = random.randint(frequence := properties["frequency"], frequence*2)
                self.add_blob(
                    properties["block"],
                    random.randint(properties["min_blob_size"], properties["max_blob_size"]),
                    random.randint(properties["min_y"], properties["max_y"]),
                    STONES,
                    properties["is_ore"]
                )

    def add_blob(self, block, nb, y, to_replace=STONES, is_ore=False):
        def can_go_on(x, y):
            try:
                return self.resume_world[x][y][0].upper() in to_replace
            except IndexError:
                return False

        if not hasattr(to_replace, "__contains__"):
            to_replace = [to_replace]
        blocks_pos = [(-1, y), (-2, y)]

        while nb > 0:
            finish = False
            n_ = 0
            while not finish:
                case: tuple = random.choice(blocks_pos)

                n_ += 1
                if n_ > 100:
                    print(y, blocks_pos)
                    exit()
                x_inc, y_inc = random.choice([(0, 1), (1, 0), (0, -1), (-1, 0)])
                x = case[0] + x_inc
                y = case[1] + y_inc
                if 0 <= y < HEIGHT_WORLD and (x, y) not in blocks_pos:
                    count = 0
                    for x_inc in (-1, 0, 1):
                        for y_inc in (-1, 0, 1):
                            if 0 <= y+y_inc < HEIGHT_WORLD and (x+x_inc, y+y_inc) in blocks_pos:
                                count += 1
                    if count >= 2:
                        finish = True
                        blocks_pos.append((x, y))

            nb -= 1
        for x, y in blocks_pos:
            if x < 0 and can_go_on(x, y):
                block = (block[0], block[1].copy())
                if is_ore:
                    block[1]["name_fond"] = self.resume_world[x][y][0]
                self.resume_world[x][y] = block
            else:
                self.__to_put.append({
                    "block": (block[0], block[1].copy()),
                    "is_ore": is_ore,
                    "x": x,
                    "y": y,
                    "condition": can_go_on
                })
