import random
from pygame.mixer import Channel, Sound
import time


class Category:
    def __init__(self, morceaux, id_, sound_manager, category_name):
        self.morceaux: dict[str, list[Sound]] = morceaux
        self.channel = Channel(id_)
        self.next_sound = time.time()
        self.sound_manager = sound_manager
        self.category_name = category_name

    def __call__(self, name, sleep=False):
        name = str(name)
        act_time = time.time()
        if self.next_sound < act_time:
            sound = random.choice(self.morceaux[name])
            self.channel.play(sound)
            self.next_sound = act_time + sound.get_length() - (0.1 if sleep else 0.4)

    def update_volume(self):
        new_volume = self.sound_manager.volumes[self.category_name] * self.sound_manager.volumes["global"]
        self.channel.set_volume(new_volume)

    def every_second(self):
        self.update_volume()
