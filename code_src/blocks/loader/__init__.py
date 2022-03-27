"""Package chargant le fichier blocks.yml,
et créant le dict blocks qui sert a autoset les attributs des objets Block"""
import yaml
import pygame
from . import img_modifier
from ...roots import SRC_ROOT

with open(SRC_ROOT / "blocks.yml") as file:
    blocks_loaded: dict[str, dict] = yaml.load(file, yaml.FullLoader)


def calculate_average_color(surface: pygame.Surface):
    sums = [0]*3
    nb_pixels = 0
    for x in range(surface.get_width()):
        for y in range(surface.get_height()):
            color = surface.get_at((x, y))
            if len(color) >= 4 and color[3] != 255:
                continue
            for c in range(3):
                sums[c] += color[c]
            nb_pixels += 1
    if nb_pixels == 0:
        return None
    return [c_sum/nb_pixels for c_sum in sums]


def parse_value(value: dict, name: str):
    color = value.pop("color", None)
    load_img = value.pop("load_img", True)
    if not load_img:
        img = None
    elif color is None:
        path_img = SRC_ROOT / f"blocks{value.pop('folder')}" / (name+".png")
        value["img"] = img = pygame.image.load(path_img)
    else:
        value["img"] = img = pygame.Surface((1, 1))
        img.fill(color)
    nb_frames = value.pop("frame_number", None)
    if nb_frames is not None:
        value["imgs"], value["nb_frames"] = imgs, _ = img_modifier.cut_img(img, nb_frames)
        value["img"] = imgs[0]
    if "img" in value:
        value["average_color"] = calculate_average_color(value["img"])
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
