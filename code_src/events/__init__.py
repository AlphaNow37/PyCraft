from .. import Game
import pygame
from ..constants import *
from ..interfaces import MenuInterface
from .keymap import KeyChangeError, KeyMapManager

"""
Event: gere les évenements du jeu
"""


class EventManager:
    def __init__(self, game: Game):
        self.game: Game = game
        self.player = game.player
        self.f3_used = False

    def events(self):
        chat_just_opened = False
        pressed = pygame.key.get_pressed()
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                self.game.running = False
            elif event.type == pygame.WINDOWRESIZED:
                self.game.size_screen = (event.x, event.y)
                self.game.size_block = get_blocks_size(self.game.size_screen, self.game.zoom)
            elif self.game.interface is None:
                if event.type == pygame.MOUSEWHEEL:
                    if event.y < 0:
                        for _ in range(abs(event.y)):
                            self.game.zoom = round(self.game.zoom*1.2)
                    else:
                        for _ in range(event.y):
                            self.game.zoom = max(4, round(self.game.zoom/1.2))
                    self.game.size_block = get_blocks_size(self.game.size_screen, self.game.zoom)
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    # pos = event.pos
                    pass

                elif event.type == pygame.KEYDOWN:
                    if not self.game.open_chat:
                        if event.key in KeyMapManager["chat"]:
                            self.game.chat_manager.open_chat()
                            chat_just_opened = True
                        elif event.key == pygame.K_n or (event.key == pygame.K_F3 and pressed[pygame.K_n]):
                            if pressed[pygame.K_F3]:
                                self.change_gamemode()
                                self.f3_used = True
                        elif event.key == pygame.K_TAB:
                            self.game.interface = MenuInterface(self.game)
                    elif event.key == pygame.K_TAB:
                        self.game.chat_manager.close_chat()
                    else:
                        self.game.chat_manager.event(event)
                    """print({
                        getattr(pygame, name): name
                        for name in dir(pygame)
                        if name.startswith("K_")
                    }[event.key])"""

                elif event.type == pygame.KEYUP:
                    if not self.game.open_chat:
                        if event.key == pygame.K_F3 and not self.f3_used:
                            self.game.open_f3 = not self.game.open_f3

                elif event.type == pygame.MOUSEMOTION:
                    pass

                elif event.type == pygame.TEXTINPUT and self.game.open_chat and not chat_just_opened:
                    self.game.chat_manager.event(event)
            elif self.game.interface is not None:
                if event.type == pygame.KEYDOWN and event.key == pygame.K_TAB:
                    if pressed[pygame.K_LSHIFT]:
                        self.game.interface.back()
                    else:
                        self.game.interface = None
                else:
                    self.game.interface.on_event(event)
        if self.game.interface is None and not self.game.open_chat:
            if KeyMapManager.is_pressed(pressed, "jump"):
                if self.game.gamemode == "SPECTATOR":
                    self.player.move(0, 1)
                else:
                    self.player.jump()
            if KeyMapManager.is_pressed(pressed, "left"):
                self.player.move(-1, 0)
            if KeyMapManager.is_pressed(pressed, "sneak"):
                self.player.move(0, -1)
            if KeyMapManager.is_pressed(pressed, "right"):
                self.player.move(1, 0)

            if not pressed[pygame.K_F3]:
                self.f3_used = False

            if KeyMapManager.is_pressed(pressed, "sneak") != self.player.sneaking:
                if self.game.gamemode != "SPECTATOR":
                    self.player.set_sneaking(pressed[pygame.K_LSHIFT] or pressed[pygame.K_s])

    def change_gamemode(self):
        self.game.change_gamemode(GAMEMODES[(GAMEMODES.index(self.game.gamemode) + 1) % len(GAMEMODES)])


def get_blocks_size(size_screen, zoom):
    width_sc, height_sc = size_screen
    width = width_sc/(zoom*2)
    height = height_sc/(zoom*2)
    size = max(width, height)
    return size
