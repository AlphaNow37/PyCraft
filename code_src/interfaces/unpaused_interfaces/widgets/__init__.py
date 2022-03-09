import pygame
from .... import Game


class Widget:
    def __init__(self, game):
        self.game: Game = game

    def draw(self, surface: pygame.Surface):
        pass
