from .VegetationGenerator import VegetationGenerator
from . import structures
from .seeder import random
from ..constants import HEIGHT_OCEAN
from .generation_blocks import BLOCKS


times = [
    (10, 20),
    (20, 60),
    (20, 50),
]


class StructGenerator(VegetationGenerator):
    def __init__(self):
        super().__init__()
        self.__next_struct = [random.randint(*times[i]) for i in range(3)]
        self.__to_put = []
        self.__to_put_foundations = []

    def generate(self):
        super().generate()
        self.puts(self.__to_put)
        for i_struct, time_before_next in enumerate(self.__next_struct):
            if time_before_next > 0:
                self.__next_struct[i_struct] -= 1
            if time_before_next-1 <= 0:
                struct: None | structures.Struct | str = None
                y_base = self.tops[-1]
                if i_struct == 0:
                    if y_base > HEIGHT_OCEAN:
                        if self.biome == "desert":
                            struct = "micro_desert_temple"
                        elif self.biome == "plain":
                            struct = "house"
                elif i_struct == 1:
                    y_base = random.randint(0, y_base-5)
                    struct = "generator"
                elif i_struct == 2:
                    y_base = random.randint(0, y_base-30)
                    struct = "lava_lake"
                if struct is not None:
                    if isinstance(struct, str):
                        struct: structures.Struct = structures.structs[struct]
                    coords = struct.get_coords(-(struct.width//2), y_base, random.randint(0, 1))
                    self.__next_struct[i_struct] = struct.width + random.randint(*times[i_struct])
                    self.__to_put.extend([
                        {"x": x, "y": y, "block": block}
                        for ((x, y), block) in coords.items()
                    ])
                    if struct.foundation is not None:
                        for x in range(struct.width):
                            x = -x+struct.width//2+1
                            name, block_data = random.choice(struct.foundation)
                            block = BLOCKS[name]
                            block = (block[0], block[1] | block_data)
                            self.__to_put_foundations.append([x, block, y_base])
        i = 0
        while i < len(self.__to_put_foundations):
            self.__to_put_foundations[i][0] -= 1
            x, block, y_base = self.__to_put_foundations[i]
            if x < 0:
                if self.tops[x] < y_base:
                    self.resume_world[x][self.tops[x]+1: y_base+1] = [block] * (y_base - self.tops[x])
                del self.__to_put_foundations[i]
            else:
                i += 1
