import pygame
from code_src import Game
from code_src.tools import PygameText


class Widget:
    height = 30
    width = 170

    def __init__(self, game: Game, column, line):
        """
        Un widget est une case sur une interface pausée
        :param game: l'instance du jeu
        :param column: le numero de la colonne /2
        :param line: le numero de la ligne
        """
        x = 5 + 180 * column
        y = line * self.height * 1.3
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

class Slider(Text):
    barre_width = 5

    def __init__(self, game: Game, column, line, text: str, func, value, **kwargs):
        super().__init__(game, column, line, text, **kwargs)
        self.func = func
        self.value = value
        self.last_slider_value = value
        self.clicking = False

    def draw(self, y, factor):
        super().draw(y, factor)
        wid_left = self.x * factor
        y = (self.y + y) * factor
        if pygame.mouse.get_pressed()[0] and self.clicking:
            mouse_x = pygame.mouse.get_pos()[0]
            mouse_x -= self.barre_width * factor / 2
            if mouse_x < wid_left:
                mouse_x = wid_left
                self.last_slider_value = 0
            else:
                x = mouse_x - wid_left
                x /= factor
                if x > self.width-self.barre_width:
                    mouse_x = (self.width-self.barre_width) * factor + wid_left
                    self.last_slider_value = 1
                else:
                    self.last_slider_value = x / (self.width-self.barre_width)
            x = mouse_x
        else:
            x = wid_left + self.value * (self.width-self.barre_width) * factor
            if self.clicking:
                self.value = self.last_slider_value
                self.func(self, self.value)
                self.clicking = False

        rect = [x, y, self.barre_width * factor, self.height * factor]
        pygame.draw.rect(self.game.screen, "grey", rect)

    def on_event(self, event: pygame.event.Event):
        if event.type == pygame.MOUSEBUTTONUP:
            self.value = self.last_slider_value
            self.func(self, self.value)
            self.clicking = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            self.clicking = True
