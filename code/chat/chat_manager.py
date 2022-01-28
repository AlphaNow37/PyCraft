from .constants import *
from ..utilitaire import PygameText
from .. import Game
import pygame
from . import command
import pyperclip


class Chatmanager:
    font = pygame.font.Font(None, 200)
    barre_change_time = 5

    def __init__(self, game: Game):
        self.lines_surfaces: list[PygameText] = []
        self.game: Game = game
        self.input = ""
        self.barre_index = 0
        self.update_input()
        self.next_back = 15
        self.lasts_inputs = []
        self.last_input_index = 0

        self.next_barre_vue_change = self.barre_change_time
        self.barre_type = True

    def event(self, event: pygame.event.Event):
        pressed = pygame.key.get_pressed()
        if event.type == pygame.KEYDOWN:
            key = event.key
            if key == pygame.K_BACKSPACE:
                self.input = self.input[:self.barre_index-1] + self.input[self.barre_index:]
                if self.barre_index != 0:
                    self.barre_index -= 1
            elif key == pygame.K_RETURN:
                self.lasts_inputs.append(self.input)
                self.send(self.input)
                if self.input.startswith("/"):
                    command.execute(self.input, self.game)
                self.input = ""
                self.barre_index = 0
            elif (pressed[pygame.K_LCTRL] or pressed[pygame.K_RCTRL]) and key == pygame.K_v:
                # If ctrl+v
                text = pyperclip.paste()
                self.input += text
                self.barre_index += len(text)
            elif key == pygame.K_UP and self.last_input_index != -len(self.lasts_inputs):
                self.last_input_index -= 1
                self.input = self.lasts_inputs[self.last_input_index]
                self.barre_index = len(self.input)
            elif key == pygame.K_DOWN and self.last_input_index != 0:
                self.last_input_index += 1
                if self.last_input_index == 0:
                    self.input = ""
                else:
                    self.input = self.lasts_inputs[self.last_input_index]
                self.barre_index = len(self.input)
            elif key == pygame.K_LEFT and self.barre_index > 0:
                self.barre_index -= 1
            elif key == pygame.K_RIGHT and self.barre_index < len(self.input):
                self.barre_index += 1
        elif event.type == pygame.TEXTINPUT:
            self.input = self.input[:self.barre_index] + event.text + self.input[self.barre_index:]
            self.barre_index += len(event.text)
        self.update_input()

    def update_input(self):
        self.inputs_surfaces = [
            self.font.render(f">>>{self.input[:self.barre_index]}{char}{self.input[self.barre_index:]}",
                             True, [255]*3, [0]*3)
            for char in ["|", " "]
        ]
        for surface in self.inputs_surfaces:
            surface.set_alpha(ALPHA)

    def draw(self):
        self.next_barre_vue_change -= 1
        if self.next_barre_vue_change <= 0:
            self.next_barre_vue_change = self.barre_change_time
            self.barre_type = not self.barre_type
        input_surface = self.inputs_surfaces[self.barre_type]
        input_height = HEIGHT_LINE*self.game.size_screen[1]/480 * 1.4
        input_width = input_height * input_surface.get_width() / input_surface.get_height()
        new_input_surface = pygame.transform.scale(input_surface, (int(input_width), int(input_height)))
        y = self.game.size_screen[1]-input_height
        self.game.screen.blit(new_input_surface, (0, y))
        for line in self.lines_surfaces[::-1]:
            y -= HEIGHT_LINE*self.game.size_screen[1]/480*(line.text.line_counter("\n") + 1)
            y -= PAD*2 * self.game.size_screen[1] / 480
            y += 1
            line.draw_xy_exact(0, y)

    def open_chat(self):
        pygame.key.start_text_input()
        self.game.open_chat = True
        self.input = ""
        self.next_back = 15

    def close_chat(self):
        pygame.key.stop_text_input()
        self.game.open_chat = False

    def send(self, text, error=False):
        pgt = PygameText(self.game, 0, 0, None, text,
                         color_text="red" if error else "white", color_fond="black",
                         height=HEIGHT_LINE*(text.line_counter("\n") + 1), pad=PAD, alpha=ALPHA)
        self.lines_surfaces.append(pgt)

    def tick(self):
        pressed = pygame.key.get_pressed()
        if pressed[pygame.K_BACKSPACE]:
            self.next_back -= 1
            if self.next_back == 0:
                self.event(pygame.event.Event(pygame.KEYDOWN, key=pygame.K_BACKSPACE))
                self.next_back = 1
        else:
            self.next_back = 15
