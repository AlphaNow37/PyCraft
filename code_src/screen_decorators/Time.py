from .. import Game
import pygame
import math
from .Property import Property
from ..constants import TIME_INCREMENT
from ..roots import SRC_ROOT
from .skycolor import get_colors


SUNRISE_TIME = 100  # Time beetween the sky color will change
MIDDLE_SUNRISE_TIME = SUNRISE_TIME/2

BEGIN_SUNRISE = 90-MIDDLE_SUNRISE_TIME  # Sunrise = lever du soleil
END_SUNRISE = 90+MIDDLE_SUNRISE_TIME

BEGIN_SUNSET = 270-MIDDLE_SUNRISE_TIME  # Sunset = coucher du soleil
END_SUNSET = 270+MIDDLE_SUNRISE_TIME


class Astre:
    def __init__(self, name, game: Game):
        self.image = pygame.image.load(SRC_ROOT / "environnement" / (name+".png"))
        self.game = game

    def draw(self, width, x, y):
        image = pygame.transform.scale(self.image, (width, width))
        self.game.screen.blit(image, (x-width/2, y-width/2))


class TimeManager:
    def __init__(self, game):
        self.game: Game = game
        self.time = Property(reset=lambda self: setattr(self, "value", 90))

        self.sun = Astre("sun_2", game)
        self.moon = Astre("Moon_2", game)

    def draw(self):
        sky_color, _ = get_colors(int(self.time))
        self.game.screen.fill(sky_color)
        angle = self.time % 360
        angle = math.radians(angle)

        width_sc, height_sc = self.game.size_screen
        x_center = width_sc / 2
        y_center = height_sc / 2

        width_img = int(self.game.size_block * self.game.zoom / 5)

        x = x_center + math.sin(angle) * width_sc / 2 * 0.75
        y = y_center + math.cos(angle) * height_sc / 2 * 0.75
        y = height_sc-y
        self.moon.draw(width_img, x, y)
        self.sun.draw(width_img, width_sc-x, height_sc-y)

    def tick(self):
        self.time += TIME_INCREMENT
        self.time %= 360

    def get_data(self):
        return {"time": self.time.get()}

    def set_data(self, data: dict):
        self.time.set(data["time"])

    def get_pos(self, angle):
        angle = math.radians(angle)
        x = math.sin(angle) * self.game.zoom / 2
        y = math.cos(angle) * self.game.zoom / 2
        x_player, y_player = self.game.camera_center
        x += x_player
        y += y_player
        return x, y
