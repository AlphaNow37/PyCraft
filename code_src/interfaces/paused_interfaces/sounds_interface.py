import math
from .abc import BasePausedInterface
from . import menu_interface
from .widgets import Button, Slider

volumes_names = ["block"]

class SoundsInterface(BasePausedInterface):
    title_text = "Sounds :"

    def __init__(self, game):
        self.superior = menu_interface.MenuInterface
        self.reset_button = Button(game, 0.5, math.ceil(len(volumes_names) / 2 + 2), self.reset,  "Reset")
        super().__init__(game)

    def reload_widgets(self):
        self.global_volume_slider = Slider(self.game, 0.5, 1, "Global volume",
                                           self.on_slider_change, self.game.sound_manager.volumes["global"])
        self.widgets = [self.global_volume_slider]
        for i, volume_name in enumerate(volumes_names):
            self.widgets.append(Slider(self.game, i % 2, i//2+2, volume_name,
                                       self.on_slider_change, self.game.sound_manager.volumes[volume_name]))

        self.widgets.append(self.reset_button)

    def reset(self):
        self.game.sound_manager.reset_volume()
        self.reload_widgets()

    def on_slider_change(self, slider, value):
        if slider is self.global_volume_slider:
            self.game.sound_manager.change_volume("global", value)
        else:
            index = self.widgets.index(slider) - 1
            self.game.sound_manager.change_volume(volumes_names[index], value)
