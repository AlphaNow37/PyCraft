"""Module chargant le fichier items.yml"""
from ..roots import SRC_ROOT
import yaml


with open(SRC_ROOT / "items.yml") as file:
    raw_items = yaml.load(file, yaml.FullLoader)

items: dict[str, dict[...]] = {}

for prefix, value in raw_items.pop("_TOOLS").items():
    for item_type in ["pickaxe", "axe", "sword", "hoe"]:
        items[f"{prefix}_{item_type}"] = value | {"item_type": item_type}
