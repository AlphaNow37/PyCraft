import pygame
from ... import Game
from . import widgets as wid
from ..abc import AbcInterface


class BasePausedInterface(AbcInterface):
    """Classe abstraite d'une interface de base"""
    bg = "#545454"
    paused = True
    widgets: list[wid.Widget] = []
    title_text: str | None = None
    title: wid.Text | None = None
    superior = None

    def __init__(self, game: Game):
        super().__init__(game)
        self.y = 0
        self.screen = game.screen
        if self.title_text is not None:
            self.set_title(self.title_text)
        self.tick()

    def on_event(self, event: pygame.event.Event):
        if event.type == pygame.MOUSEWHEEL:
            max_y = (max(w.y + w.height for w in self.widgets)  # Le coté le plus bas
                     - 360*(self.game.size_screen[1]/self.game.size_screen[0]))
            # Si la fenetre est peu haute, il faut ajouter de la marge
            self.y += event.y * 30
            self.y = min(0, (max(-max_y, self.y)))
            return
        else:
            x = y = None
            match event.__dict__:
                case {"x": x, "y": y}:
                    pass
                case {"pos": (x, y)}:
                    pass
            if x is not None:
                x /= self.factor
                y /= self.factor
                y += self.y
                for btn in self.widgets:
                    if btn.rect.collidepoint(x, y):
                        btn.on_event(event)

    def draw(self):
        self.screen.fill(self.bg)
        for btn in self.widgets:
            btn.draw(self.y, self.factor)
        if self.title is not None:
            self.title.draw(self.y, self.factor)

    def tick(self):
        self.factor = self.game.size_screen[0] / 360

    def change_interface(self, new_interface_class):
        if new_interface_class is None:
            self.close()
        else:
            self.game.interface = new_interface_class(self.game)

    def set_title(self, text):
        self.title = wid.Text(self.game, 0.5, 0, text)

    def back(self):
        if self.superior is None:
            self.close()
        else:
            self.game.interface = self.superior(self.game)
