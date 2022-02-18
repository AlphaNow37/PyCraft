from pygame.mixer import Channel
from ..roots import SRC_ROOT
from .. import Game
from . import loader
import random

sounds = loader.sounds

SOUNDS_ROOT = SRC_ROOT / "sounds"


class SoundManager:
    def __init__(self, game):
        self.game: Game = game
        self.breaked_channel = Channel(1)

    def tick(self):
        pass

    def change_volume(self, categorie_name: str):
        pass

    def play_breaked_sound(self, name):
        print(name)
        sound = random.choice(sounds["breaked"][name])
        self.breaked_channel.play(sound)
