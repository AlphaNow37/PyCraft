import random
from pygame.mixer import Channel, Sound
import time


class Category:
    def __init__(self, morceaux, id_):
        self.morceaux: dict[str, list[Sound]] = morceaux
        self.channel = Channel(id_)
        self.next_sound = time.time()

    def __call__(self, name, sleep=False):
        name = str(name)
        act_time = time.time()
        if self.next_sound < act_time:
            sound = random.choice(self.morceaux[name])
            self.channel.play(sound)
            self.next_sound = act_time + sound.get_length() - (0.1 if sleep else 0.4)
