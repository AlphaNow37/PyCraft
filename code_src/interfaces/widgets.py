import pygame
from .. import Game
from ..utilitaire import PygameText


class Widget:
    height = 30
    width = 170

    def __init__(self, game: Game, column, line):
        x = 5 + 180 * column
        y = line * self.height
        self.x = x
        self.y = y
        self.rect = pygame.Rect(x, y, self.width, self.height)
        self.game = game

    def draw(self, y, factor):
        pass

    def on_event(self, event):
        pass


class Text(Widget):
    def __init__(self, game: Game, column, line, text: str, **kwargs):
        super().__init__(game, column, line)
        text = text.center(30)
        self.text = PygameText(game, self.x, self.y, text=text, **kwargs)

    def draw(self, y, factor):
        if int(self.y) == 1017:
            print(y+self.y, (y+self.y) * factor, self.game.size_screen[1])
        self.text.draw_with_size(
            self.text.x * factor, (y+self.y) * factor,
            self.width * factor, self.height * factor)


class Button(Text):
    def __init__(self, game: Game, column, line, func, text: str, **kwargs):
        super().__init__(game, column, line, text, **kwargs)
        self.func = func

    def on_event(self, event: pygame.event.Event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            self.func()
