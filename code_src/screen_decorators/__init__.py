from .. import Game
from . import Clouds
from . import Time
from . import BreakerPlacer
from . import Block_overlay
from . import F3_screen
from . import Weather
from . import player_bar

from . import cursor_and_icon as _  # we just run the file


class ScreenDecorator:
    # NOTE: decorator != decoration
    #       |               \-> the moon, the sky, the rain, the weather, the overlays
    #       \-> @truc <\n> def ...
    """Classe servant a centraliser les décorations"""

    def __init__(self, game: Game):
        self.game: Game = game

        self.cloud_manager = Clouds.CloudManager(game)
        self.time_manager = Time.TimeManager(game)
        self.breaker_manager = BreakerPlacer.BreakerPlacerManager(game)
        self.block_overlay_manager = Block_overlay.BlockOverlayManager(game)
        self.f3_manager = F3_screen.F3ScreenManager(game)
        self.weather_manager = Weather.WeatherManager(game)
        self.player_bar_manager = player_bar.PlayerBarManager(game)

    def draw_clouds(self):
        self.cloud_manager.draw()

    def draw_sun_moon_sky_weather(self):
        self.time_manager.draw()
        self.weather_manager.draw()

    def draw_overlays(self):
        self.block_overlay_manager.draw()
        self.breaker_manager.draw()

    def tick(self):
        self.cloud_manager.tick()
        self.time_manager.tick()
        self.breaker_manager.tick()


    def draw_f3_screen(self):
        self.f3_manager.draw()

    def get_data(self):
        return self.time_manager.get_data() | self.weather_manager.get_data()

    def set_data(self, data):
        self.weather_manager.set_data(data)
        self.time_manager.set_data(data)

    def draw_bars(self):
        self.player_bar_manager.draw()
