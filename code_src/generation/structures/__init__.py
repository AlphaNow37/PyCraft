import pathlib
import re
import json

from .. import generation_blocks
from ..seeder import random
blocks = generation_blocks.BLOCKS
search_path = pathlib.Path(__file__).parent

regex_json = re.compile(r"(?P<name>.+)(?P<json>{.*})")

class Struct:
    def __init__(self, name):
        with open(search_path / f"{name}.struct") as file:
            content: str = file.read()
        meta, data = content.split("\n---\n")
        lines = (map(str.strip, line.split(":", 1)) for line in meta.split("\n"))
        self.keys = key_blocks = dict(lines)
        for key, value in key_blocks.items():
            blocks = value.split("|")
            for i, block in enumerate(blocks):
                if res := regex_json.fullmatch(block):
                    group = res.groupdict()
                    name = group["name"]
                    block_data = json.loads(group["json"])
                else:
                    name = block
                    block_data = {}
                blocks[i] = (name, block_data)
            key_blocks[key] = blocks
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
        coords = {}
        for (x_, y_), value in self.coords.items():
            if x_inversed:
                x_block = x+self.width-x_-1
            else:
                x_block = x+x_
            y_block = y+y_
            name, block_data = random.choice(self.keys[value])
            if x_inversed and "flip_x" in block_data:
                block_data = block_data.copy()
                block_data["flip_x"] = not block_data["flip_x"]
            block = blocks[name]
            block = (block[0], block[1] | block_data)
            coords[(x_block, y_block)] = block
        return coords


structs: dict[str, Struct] = {}
for name in ["micro_desert_temple", "generator", "house", 'lava_lake']:
    structs[name] = Struct(name)
