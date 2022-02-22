from ..roots import SRC_ROOT
from .. import Game
from . import loader
from .catagory import Category

sounds = loader.sounds

SOUNDS_ROOT = SRC_ROOT / "sounds"


class SoundManager:
    """Interface permettant de jouer des sons"""
    def __init__(self, game):
        self.game: Game = game
        self.breaked = Category(sounds["breaked"], 0)

    def tick(self):
        pass

    def change_volume(self, categorie_name: str):
        pass
