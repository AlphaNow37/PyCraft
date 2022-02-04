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
                ("save", self.save_world),
                ("open", self.open_world),
            ])
        ]

    def open_world(self):
        def on_finish(text: str):
            text = text.strip()
            if not text:
                return False, "You must to specify a name"
            else:
                try:
                    self.game.open_world(text)
                except ValueError as e:
                    return False, str(e)
            return True, "Succefully opened the world"
        self.change_interface(None)
        self.game.chat_manager.start_input(on_finish, "Enter the name of the world")

    def save_world(self):
        def on_finish(text: str):
            print("tt")
            text = text.strip()
            if not text:
                return False, "You must to specify a name"
            else:
                try:
                    self.game.save_world(text)
                except ValueError:
                    return False, "Invalid name"
            return True, "Succefully saved the world"
        self.change_interface(None)
        self.game.chat_manager.start_input(on_finish, "Enter the name of the world")
