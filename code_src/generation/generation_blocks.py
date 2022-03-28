from ..blocks import loader as block_loader

FLEURS_NAMES = [
                   [name, ] for name in
                   ["pink", "blue", "yellow", "red",
                    "white_tulip", "pink_tulip", "red_tulip",
                    ]] + [
                   [name + "_0", name + "_1"] for name in
                   ["violet", "red2", "pink2"]]
FLEURS_BLOCKS_NAMES = [f"fleur_{name}" for flor in FLEURS_NAMES for name in flor]

BLOCKS = {
    name.upper(): (name, {"class": val.get("class")})
    for name, val in block_loader.blocks.items()
}

STONES = ["GRANITE", "DIORITE", "ANDESITE", "STONE"]
WATER_PATCHES_BLOCKS = ["SAND", "SAND", "DIRT", "GRAVEL"]

COLORS_TERRACOTTA = [
    "red",
    "yellow",
    "orange",
    "red",
    "orange",
    "yellow",
    "orange",
    "white",
    "gray",
    "black",
    "brown",
    "red",
    "yellow",
    "orange",
    "pink",
]
