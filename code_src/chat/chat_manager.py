from .constants import *
from .. import Game
import pygame
from . import command
import pyperclip
from typing import Generator
from ..font import get_text, FONTSIZE, get_surface_line


class Chatmanager:
    """Interface du chat"""
    font = pygame.font.Font(None, 200)
    barre_change_time = 5

    def __init__(self, game: Game):
        self.lines_surfaces: list[pygame.Surface] = []
        self.game: Game = game
        self.input = ""
        self.barre_index = 0
        self.update_input()
        self.next_back = 15
        self.lasts_inputs = []
        self.last_input_index = 0
        self.on_input = False

        self.next_barre_vue_change = self.barre_change_time
        self.barre_type = True

        self.active_command: Generator | None = None

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
                if self.active_command is not None:
                    self.send(f">>> {self.input}")
                    try:
                        self.active_command.send(self.input)
                    except (StopIteration, RuntimeError):
                        self.active_command = None
                else:
                    self.send(f"[You] {self.input}")
                self.last_input_index = 0
                if self.on_input:
                    self.finish_input(self.input)
                elif self.input.startswith("/"):
                    res = command.execute(self.input, self.game)
                    if isinstance(res, Generator):
                        try:
                            next(res)
                            self.active_command = res
                        except (StopIteration, RuntimeError):
                            pass
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
            get_surface_line(f">>>{self.input[:self.barre_index]}{char}{self.input[self.barre_index:]}",
                             "white", "black")
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
        height_line = self.game.size_screen[1] * 1/25
        input_width = height_line * input_surface.get_width() / input_surface.get_height()
        new_input_surface = pygame.transform.scale(input_surface, (int(input_width), int(height_line*1.4)))
        coef = height_line/(FONTSIZE+1)
        y = self.game.size_screen[1]-height_line*1.4
        self.game.screen.blit(new_input_surface, (0, y))
        for line in self.lines_surfaces[::-1]:
            new_height = line.get_height()*coef
            new_width = new_height * line.get_width() / line.get_height()
            y -= new_height
            y += 1
            line = pygame.transform.scale(line, (new_width, new_height))
            self.game.screen.blit(line, (0, y))

    def open_chat(self):
        pygame.key.start_text_input()
        self.game.open_chat = True
        self.input = ""
        self.next_back = 15

    def close_chat(self):
        pygame.key.stop_text_input()
        self.game.open_chat = False

    def send(self, text, error=False):
        surface = get_text(text, ALPHA, "red" if error else "white", "black", padx=PAD, pady=PAD)
        self.lines_surfaces.append(surface)

    def tick(self):
        pressed = pygame.key.get_pressed()
        if pressed[pygame.K_BACKSPACE]:
            self.next_back -= 1
            if self.next_back == 0:
                self.event(pygame.event.Event(pygame.KEYDOWN, key=pygame.K_BACKSPACE))
                self.next_back = 1
        else:
            self.next_back = 15

    def start_input(self, command_finish, text):
        self.on_input = True
        self.command_finish = command_finish
        self.send(f"[Input] {text} :")
        self.open_chat()

    def finish_input(self, text):
        if text in ("...", "/", "stop"):
            self.stop_input("Exiting", error=True)
        res = self.command_finish(text)
        match res:
            case True:
                self.stop_input("Correct answers")
            case False:
                self.send("[Input] Incorrect answers", error=True)
            case (False, str(text)):
                self.send(f"[Input] {text}", error=True)
            case (True, str(text)):
                self.stop_input(text)
            case None:
                self.stop_input()
            case _:
                raise ValueError(f"Error: incorrect res for the finish command: {res}")

    def stop_input(self, text=None, error=None):
        if text is not None:
            self.send(f"[Input] {text}", error=error)
        self.close_chat()
        del self.command_finish
        self.on_input = False
