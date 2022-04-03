from ..roots import SRC_ROOT
from .. import Game
from . import loader
from .catagory import Category

sounds = loader.sounds

SOUNDS_ROOT = SRC_ROOT / "sounds"


class SoundManager:
    """Interface permettant de jouer des sons"""

    def __init__(self, game):
        self.volumes = {
            "global": 1,
            "block": 1,
        }
        self.game: Game = game

        self.breaked = Category(sounds["breaked"], 0, self, "block")
        self.placed = Category(sounds["breaked"], 0, self, "block")

        self.all_categories = [self.breaked, self.placed]

    def tick(self):
        if self.game.tick % 20 == 0:
            for cat in self.all_categories:
                cat.every_second()

    def change_volume(self, categorie_name: str, new_volume):
        self.volumes[categorie_name] = new_volume

    def reset_volume(self):
        self.change_volume("global", 1)
        self.change_volume("block", 1)
