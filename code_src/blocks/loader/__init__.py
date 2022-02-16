"""Package chargant le fichier blocks.yml"""
import yaml
import pygame
import pathlib
from . import img_modifier
from ...roots import SRC_ROOT
search_path = pathlib.Path(__file__).parent

with open(search_path / "blocks.yml") as file:
    blocks_loaded: dict[str, dict] = yaml.load(file, yaml.FullLoader)


def parse_value(value: dict, name: str):
    color = value.pop("color", None)
    load_img = value.pop("load_img", True)
    if not load_img:
        pass
    elif color is None:
        path_img = SRC_ROOT / f"blocks{value.pop('folder')}" / (name+".png")
        value["img"] = pygame.image.load(path_img)
    else:
        value["img"] = img = pygame.Surface((1, 1))
        img.fill(color)
    blocks[name] = value
    return value


def register_block(value: dict, name: str):
    stair = value.pop("stair", False)
    slab = value.pop("slab", False)
    value = parse_value(value.copy(), name)
    img = value.get("img")
    if stair:
        stair_modifiers = {
            "img": img_modifier.get_stair_img(img), "load_img": False,
            "support_x_flip": True, "support_y_flip": True,
        }

        parse_value(value | stair_modifiers, f"{name}_stair")
    if slab:
        slab_mofidier = {
            "img": img_modifier.get_slab_img(img), "load_img": False,
            "support_y_flip": True, "height": 0.5, "is_slab": True,
        }
        parse_value(value | slab_mofidier, f"{name}_slab")


blocks: dict[str, dict] = {}
for name_block, block in blocks_loaded.items():
    block = block.copy()
    block: dict
    if name_block.startswith("_"):
        if "into" in block:
            intos = block.pop("into")
            start_add = block.get("prefix", "")
            end_add = block.get("suffix", "")
            for name_into in intos:
                name_into = start_add + name_into + end_add
                register_block(block.copy(), name_into)
    else:
        name = block.pop("name", name_block)
        register_block(block, name)

# import json
# print(json.dumps(blocks, default=repr, indent=4))
