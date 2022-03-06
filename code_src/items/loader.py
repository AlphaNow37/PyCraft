"""Module chargant le fichier items.yml"""
from ..roots import SRC_ROOT
import yaml


with open(SRC_ROOT / "items.yml") as file:
    raw_items = yaml.load(file, yaml.FullLoader)

items: dict[str, dict[...]] = {}

for prefix, value in raw_items.pop("_TOOLS").items():
    for suffix in ["pickaxe", "axe", "sword", "hoe"]:
        items[f"{prefix}_{suffix}"] = value | {f"is_{suffix}": True}
