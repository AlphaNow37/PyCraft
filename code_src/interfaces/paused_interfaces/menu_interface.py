from .abc import BasePausedInterface
from .widgets import Button, Widget
from functools import partial
from . import keys_interface
from . import sounds_interface


class MenuInterface(BasePausedInterface):
    title_text = "Menu :"

    def reload_widgets(self):
        self.widgets: list[Widget] = [
            Button(self.game, i % 2, i//2+1, func, text=text, color_fond="grey", color_text="black")
            for (i, (text, func)) in enumerate([
                ("Keys", partial(self.change_interface, keys_interface.KeyInterface)),
                ("Sounds", partial(self.change_interface, sounds_interface.SoundsInterface)),
                ("", lambda: None),
                ("reset", lambda: [self.game.reset_world(), self.change_interface(None)]),
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
        self.close()
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
        self.close()
        self.game.chat_manager.start_input(on_finish, "Enter the name of the world")
