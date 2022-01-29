import random as rdm
import sys

class Seeder:
    def __init__(self, seed=None):
        self.random = rdm.Random(None)
        self.reset(seed)

    def reset(self, seed=None):
        if seed is None:
            seed = self.get_random_seed()
        self.random.seed(seed)
        self.seed = seed

    @staticmethod
    def get_random_seed():
        return rdm.randrange(sys.maxsize)

seeder = Seeder(None)
random = seeder.random
