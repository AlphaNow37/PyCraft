from .seeder import random
from .global_tools import get_height_snow_by_temp

BIOMES = {  # (temperature, humidite)
    (1, -1): ["desert", "desert", "mesa"],
    (1, 0): "savan",
    (1, 1): "jungle",

    (0, 1): ["oak_forest", "birch_forest", "plain"],
    (0, 0): ["oak_forest", "birch_forest", "plain"],
    (0, -1): ["oak_forest", "birch_forest", "plain"],

    (-1, -1): "plain",
    (-1, 0): "spruce_forest",
    (-1, 1): "ice_peaks",


    None: ["oak_forest", "plain", "birch_forest"]
}

force_biome = "plain"
force_temp = None
force_humid = None


class BaseGenerator:
    def __init__(self):
        self.__temperature: int = 0
        self.__humidite: int = 0
        self.biomes = []
        self.__to_next_biome()
        self.x = 0

    def generate(self):
        self.__next_biome -= 1
        if self.__next_biome == 0:
            self.__to_next_biome()
        self.biomes.append((self.biome, self.__temperature, self.__humidite))
        self.x += 1

    def __to_next_biome(self):
        self.__next_biome = random.randint(15, 25)
        self.__humidite += random.choice([
            0,
            1 if self.__humidite != 1 else 0,
            -1 if self.__humidite != -1 else 0,
        ])
        self.__temperature += random.choice([
            0,
            1 if self.__temperature < 3 else 0,
            -1 if self.__temperature > -3 else 0,
        ])
        """if force_humid is not None:
            self.__humidite = force_humid
        if force_temp is not None:
            self.__temperature = force_temp"""

        new_biome = BIOMES[(int(self.__temperature/2), self.__humidite)]
        if isinstance(new_biome, list):
            new_biome = random.choice(new_biome)
        self.biome = new_biome

        self.height_snow = get_height_snow_by_temp(self.__temperature)

        if force_biome is not None:
            self.biome = force_biome

    def setup(self):
        for _ in range(20):
            self.generate()

    def remove_first_column(self):
        del self.biomes[0]
