"""This module load all the sounds files"""
from pygame.mixer import Sound

from ..roots import SRC_ROOT
SOUND_ROOT = SRC_ROOT / "sounds"

sounds: dict[str, dict[str, list[Sound]]] = {}

for dirname in ["breaked", ]:
    sounds[dirname] = local = {}
    for filename in (SOUND_ROOT / dirname).iterdir():
        name = filename.name.removesuffix(".ogg")
        if filename.is_dir():
            local[name] = lst = [Sound(subfile) for subfile in filename.iterdir()]
        else:
            local[name] = [Sound(filename)]
