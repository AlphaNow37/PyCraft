from .. import Game
import pygame
from ..constants import GameMode
from .. import interfaces
from .keymap import KeyChangeError, KeyMapManager
from .. import items
import cProfile

"""
Event: gere les évenements du jeu
"""


class EventManager:
    def __init__(self, game: Game):
        self.game: Game = game
        self.player = game.player
        self.f3_used = False
        self.key_manager = KeyMapManager()
        self.profiling = False

    def events(self):
        """
        regarde tout les évenements et réagit en conséquence
        """
        mouse_pos = pygame.mouse.get_pos()
        chat_just_opened = False
        pressed = pygame.key.get_pressed()

        hotbar = self.game.sc_deco.player_bar_manager.hotbar_manager

        for event in pygame.event.get():

            # When the window is closed
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                self.game.running = False

            # Update the block-size when the window is resized
            elif event.type == pygame.WINDOWRESIZED:
                self.game.size_screen = (event.x, event.y)
                self.game.size_block = get_blocks_size(self.game.size_screen, self.game.zoom)

            # When there is an interface, the event's catch is not the same
            elif self.game.interface is None:
                if event.type == pygame.MOUSEWHEEL:
                    if hotbar.box.collidepoint(mouse_pos):
                        # modifie the main hand position
                        hotbar.event(event)
                    else:
                        # Update the zoom
                        self.game.zoom = round(1.2**(-event.y) * self.game.zoom)
                        self.game.zoom = max(self.game.zoom, 4)
                        self.game.size_block = get_blocks_size(self.game.size_screen, self.game.zoom)

                elif event.type == pygame.MOUSEBUTTONDOWN and event.button <= 3:
                    # If the click is on the hotbar
                    if hotbar.box.collidepoint(mouse_pos):
                        hotbar.event(event)
                    # If the click is a middle click
                    elif event.button == pygame.BUTTON_MIDDLE:
                        x, y, _, _ = self.game.get_pos_from_screenpos(mouse_pos)
                        block = self.game.map.get_case(x, y)
                        if block is None or block.air:
                            continue
                        hotbar_cont = self.game.player_inventory.hotbar
                        hand_position = self.game.player_inventory.hand_position
                        if self.game.is_admin and self.game.player_inventory.get_main_hand_item() is None:
                            hotbar_cont[hand_position] = items.item.get_item(block)

                # Movements and other key events
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_F6:
                        self.profiling = not self.profiling
                        if self.profiling:
                            self.profile = cProfile.Profile()
                            self.profile.enable()
                        else:
                            self.profile.print_stats(sort="cumtime")
                            del self.profile
                        continue
                    elif not self.game.open_chat:
                        if event.key in self.key_manager["chat"]:
                            self.game.chat_manager.open_chat()
                            chat_just_opened = True
                        elif event.key == pygame.K_n or (event.key == pygame.K_F3 and pressed[pygame.K_n]):
                            if pressed[pygame.K_F3]:
                                self.next_gamemode()
                                self.f3_used = True
                        elif event.key == pygame.K_TAB:
                            self.game.interface = interfaces.MenuInterface(self.game)
                        elif event.key in self.key_manager["inventory"]:
                            self.game.interface = interfaces.InventoryInterface(self.game)
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

                # Send the texts to the chat manager
                elif event.type == pygame.TEXTINPUT and self.game.open_chat and not chat_just_opened:
                    self.game.chat_manager.event(event)

            # Else
            elif self.game.interface is not None:
                if event.type == pygame.KEYDOWN and event.key == pygame.K_TAB:
                    if pressed[pygame.K_LSHIFT]:
                        self.game.interface.back()
                    else:
                        self.game.interface.close()
                else:
                    self.game.interface.on_event(event)

        if self.game.interface is None and not self.game.open_chat:
            if self.key_manager.is_pressed(pressed, "jump"):
                if self.game.gamemode == GameMode.SPECTATOR:
                    self.player.move(0, 1)
                else:
                    self.player.jump()

            self.handle_player_moves(pressed)
            if not pressed[pygame.K_F3]:
                self.f3_used = False

    def next_gamemode(self):
        act_n = int(self.game.gamemode)
        self.game.change_gamemode(GameMode((act_n + 1) % len(GameMode)))

    def handle_player_moves(self, pressed):
        self.game.player.ia.handle_player_inputs(pressed, self.key_manager.is_pressed)


def get_blocks_size(size_screen, zoom):
    width_sc, height_sc = size_screen
    width = width_sc/(zoom*2)
    height = height_sc/(zoom*2)
    size = max(width, height)
    return size
