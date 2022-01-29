import pygame
from .. import Game
from functools import cache
import random
from ..generation import get_height_snow_by_temp
from .Property import Property
from ..constants import SRC_ROOT


FALLING_RAIN_SPEED = 1/8


class WeatherParticle:
    snow_img = pygame.image.load(SRC_ROOT / "environnement" / "snow.png")
    rain_img = pygame.image.load(SRC_ROOT / "environnement" / "rain.png")
    rain_img.set_colorkey((0, 0, 0))
    snow_img.set_colorkey((0, 0, 0))

    width = 1
    height = 4

    def __init__(self, game):
        self.game = game

    def draws(self, snowing, y):
        w, h = self.game.size_screen
        add_up = y*self.game.size_block
        src = get_surface(w, h+self.height*self.game.size_block, self.game.size_block, snowing)
        self.game.screen.blit(src, (0, -add_up))


class WeatherManager:
    def __init__(self, game):
        self.game: Game = game
        self.weather_particle = WeatherParticle(game)
        self.y = 0
        self.raining = Property(reset=(lambda prop: setattr(prop, "value", not random.randint(0, 3))))
        self.next_rain = Property(reset=(lambda prop: setattr(prop, "value", random.randint(300, 500))))

    def draw(self):
        self.next_rain -= 1
        if self.next_rain <= 0:
            self.raining.not_bool()
            self.next_rain.reset()
        if self.raining.get():
            temp = self.game.map.get_biome()[1]
            y_min = get_height_snow_by_temp(temp)
            snowing = int(y_min <= self.game.player.y-2)

            self.y -= FALLING_RAIN_SPEED
            self.y %= self.weather_particle.height
            self.weather_particle.draws(snowing, self.y)

    def get_data(self):
        return {"raining": self.raining.get(), "next_rain": self.next_rain.get()}

    def set_data(self, data: dict):
        self.raining.set(data["raining"])
        self.next_rain.set(data["next_rain"])


@cache
def get_surface(width_sc, height_sc, size_block, img_id: int):
    if img_id == 0:
        img = WeatherParticle.rain_img
    else:
        img = WeatherParticle.snow_img
    img = pygame.transform.scale(img, (size_block, size_block*4))
    surface = pygame.Surface((width_sc, height_sc))
    surface.set_colorkey((0, 0, 0))
    x = 0
    while x < width_sc:
        y = random.randint(-int(size_block*4)*100, 0)/100
        while y < height_sc:
            surface.blit(img, (int(x), int(y)))
            y += size_block * 4
        x += size_block
    return surface
