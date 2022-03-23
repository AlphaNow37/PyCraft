from . import *

dct_name_to_cls = {
    "ORE": Ore,
    "GRASS": Grass,
    "BIG_FLOWER_UP": BigFlowerUp,
    "BIG_FLOWER_BOTTOM": BigFlowerBottom,
    "SUPPORTED_BLOCK": SupportedBlock,
    "GRAVITY": GravityBlock,
    "FLUID": FluidBlock,
}
dct_cls_to_name = {
    cls: name for (name, cls) in dct_name_to_cls.items()
}

def get_cls(name, default=Block):
    if isinstance(name, type):
        return name
    elif name in dct_name_to_cls:
        pass
    else:
        name = blocks.get(name, {}).get("class")
    return dct_name_to_cls.get(name, default)

def get_name(cls, default=None):
    return dct_cls_to_name.get(cls, default)
