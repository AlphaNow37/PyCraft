import math
from .abc import BasePausedInterface
from . import menu_interface
from .widgets import Button, Slider

volumes_names = ["block"]

class SoundsInterface(BasePausedInterface):
    title_text = "Sounds :"

    def __init__(self, game):
        self.superior = menu_interface.MenuInterface
        self.global_volume_slider = Slider(game, 0.5, 1, "Global volume",
                                           self.on_slider_change, game.sound_manager.global_volume)
        self.reset_button = Button(game, 0.5, math.ceil(len(volumes_names) / 2 + 2), self.reset,  "Reset")
        super().__init__(game)

    def reload_widgets(self):
        self.widgets = [self.global_volume_slider]
        self.widgets.append(self.reset_button)

    def reset(self):
        pass

    def on_slider_change(self, slider, value):
        if slider is self.global_volume_slider:
            self.game.sound_manager.change_volume("global", value)
