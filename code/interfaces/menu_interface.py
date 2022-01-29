from .abc import BaseInterface
from .widgets import Button, Text, Widget
from functools import partial
from . import keys_interface


class MenuInterface(BaseInterface):
    title_text = "Menu :"

    def __init__(self, game):
        super().__init__(game)
        self.widgets: list[Widget] = [
            Button(game, i % 2, (i//2+1)*1.3, func, text=text, color_fond="grey", color_text="black")
            for (i, (text, func)) in enumerate([
                ("Keys", partial(self.change_interface, keys_interface.KeyInterface)),
                ("reset", lambda: [game.reset_world(), self.change_interface(None)]),
                ("save", lambda: [game.save_world(), self.change_interface(None)]),
                ("open", lambda: [game.open_world(), self.change_interface(None)]),
            ])
        ]
