from .. import Game
from ..base_elements import BaseCarre
import pygame
"""Gere le fond gris qui montre où est la souris"""

class Overlay(BaseCarre):
    img = pygame.Surface((1, 1))
    img.fill("#FFFFFF")

    alpha = 50


class BlockOverlayManager:
    def __init__(self, game: Game):
        self.overlay = Overlay(game, 0, 0)
        self.game = game

    def draw(self):
        self.overlay.x, self.overlay.y = self.game.mouse_pos
        self.overlay.draw()
