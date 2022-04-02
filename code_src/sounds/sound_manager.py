from ..roots import SRC_ROOT
from .. import Game
from . import loader
from .catagory import Category

sounds = loader.sounds

SOUNDS_ROOT = SRC_ROOT / "sounds"


class SoundManager:
    """Interface permettant de jouer des sons"""
    def __init__(self, game):
        self.global_volume = 1
        self.game: Game = game
        self.breaked = Category(sounds["breaked"], 0, self)
        self.placed = Category(sounds["breaked"], 0, self)

        self.all_categories = [self.breaked, self.placed]

    def tick(self):
        pass

    def change_volume(self, categorie_name: str, new_volume):
        match categorie_name:
            case "global":
                self.global_volume = new_volume
                for cat in self.all_categories:
                    cat.on_global_volume_change()
            case "block":
                self.breaked.change_volume(new_volume)
                self.placed.change_volume(new_volume)
