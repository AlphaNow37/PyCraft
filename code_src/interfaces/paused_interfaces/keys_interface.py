import pygame
import math

from .abc import BasePausedInterface
from .widgets import Widget, Button
from . import menu_interface
from functools import partial
from ...events.keymap import KeyChangeError


class KeyInterface(BasePausedInterface):
    """Interface gerant l'attribution des touches aux différentes actions"""
    title_text = "KeyMap :"
    superior = menu_interface.MenuInterface

    def __init__(self, game):
        super().__init__(game)
        self.key_manager = game.event_manager.key_manager
        self.reset_btn = Button(game, 0.5, math.ceil(len(self.key_manager.keys)/2)*1.3+1.3, self.reset_keys, "Reset")
        self.base_title = self.title
        self.reload_buttons()
        self.changed_key = None

    def start_change_key(self, action):
        self.changed_key = action
        self.set_title(f"KeyMap: <+: {action}>")

    def reset_keys(self):
        self.key_manager.reset()
        self.reload_buttons()

    def on_event(self, event: pygame.event.Event):
        if event.type == pygame.KEYDOWN and self.changed_key:
            try:
                self.key_manager.change_key(self.changed_key, event.key)
            except KeyChangeError:
                pass
            else:
                self.changed_key = None
                self.reload_buttons()
                self.title = self.base_title
        super().on_event(event)

    def reload_buttons(self):
        self.widgets: list[Widget] = [
            Button(self.game, i % 2, (i // 2 + 1) * 1.3,
                   partial(self.start_change_key, text),
                   text=f"{text}: {','.join(pygame.key.name(key) for key in self.key_manager.get(text))}",
                   color_fond="grey", color_text="black")
            for (i, text) in enumerate(self.key_manager.keys)
        ]
        self.widgets.append(self.reset_btn)
