import pathlib
from .. import generation_blocks
from ..seeder import random
blocks = generation_blocks.BLOCKS
search_path = pathlib.Path(__file__).parent

class Struct:
    def __init__(self, name):
        with open(search_path / f"{name}.struct") as file:
            content: str = file.read()
        meta, data = content.split("\n---\n")
        lines = (map(str.strip, line.split(":")) for line in meta.split("\n"))
        self.keys = key_blocks = dict(lines)
        for key in key_blocks:
            key_blocks[key] = key_blocks[key].split("|")
        self.foundation = key_blocks.pop("_FOUNDATION", None)
        raw_grid = [list(line) for line in data.split("\n")]
        final_dict = {
            (x, len(raw_grid)-y): id_
            for (y, line) in enumerate(raw_grid)
            for (x, id_) in enumerate(line)
            if id_ != " "
        }
        self.coords = final_dict
        self.width = max(final_dict, key=(lambda coord: coord[0]))[0] + 1
        self.height = max(final_dict, key=(lambda coord: coord[1]))[1] + 1

    def get_coords(self, x=0, y=0, x_inversed=False):
        a = {
            ((x+self.width-x_-1) if x_inversed else (x+x_), y+y_): blocks[random.choice(self.keys[value])]
            for ((x_, y_), value) in self.coords.items()
        }
        return a


structs: dict[str, Struct] = {}
for name in ["micro_desert_temple", "generator"]:
    structs[name] = Struct(name)
