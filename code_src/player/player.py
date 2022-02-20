import pygame
from ..entity import BaseEntity
import math
from ..roots import SRC_ROOT, CACHE_ROOT, USER_ROOT
from .skin_loader import get_img_from_skin, download_skin
from .. import Game
from ..constants import GRAVITY

import json
import threading

class Player(BaseEntity):
    """Classe auquel appartient uniquement le joueur"""
    username = "None"
    fragments: dict[str, dict[str, pygame.Surface] | pygame.Surface]
    fragments = get_img_from_skin(pygame.image.load(SRC_ROOT / "entity" / "player.png"))

    height = 1.9
    width = height / fragments["front"].get_height() * fragments["front"].get_width()
    img = fragments["front"]

    base_life = 100

    @classmethod
    def set_img(cls):
        """Charge le skin du joueur"""
        with open(USER_ROOT / "user.json") as file:
            user_data = json.load(file)
        cls.username = user_data["username"]
        skin_dir = CACHE_ROOT / ("skin_" + cls.username + ".png")
        if not skin_dir.exists():
            succes = download_skin(skin_dir, cls.username)
            if not succes:
                return
        base_skin = pygame.image.load(str(skin_dir))
        fragments = cls.fragments = get_img_from_skin(base_skin)
        cls.fragments = fragments
        cls.img = fragments["front"]

    def __init__(self, game: Game, y):
        super(Player, self).__init__(game, 0, 0)
        self.tp_to(0.5, y)
        self.spawnpoint = [0.5, y]
        self.vue_dir = 0
        self.sneaking = False

    def move(self, x, y):
        any_ = super().move(x, y)
        self.game.camera_center = (self.x, self.y)
        return any_

    def tick(self):
        self.fall = not self.game.gamemode == "SPECTATOR"
        self.collision = self.fall
        super(Player, self).tick()
        if self.was_destroyed:
            self.send_death_message(f"{self.username} hits the ground too hard")

    def tp_to(self, x, y):
        self.x = x
        self.y = y - self.height / 4 + 1
        self.game.camera_center = (self.x, self.y)

    def get_distance(self, x, y):
        return math.dist((self.x, self.y), (x, y))

    def update_vue_dir(self):
        x1, y1 = self.game.size_screen
        x1 /= 2
        y1 /= 2
        x2, y2 = pygame.mouse.get_pos()
        x2 -= x1
        y2 -= y1
        if x2 < 0:
            neg = True
            x2 = abs(x2)
        else:
            neg = False
        if y2 < 0:
            down = True
            y2 = abs(y2)
        else:
            down = False
        if y2 == 0:
            self.vue_dir = 0
            return
        angle = math.atan(x2 / y2)
        angle = math.degrees(angle)
        if down:
            angle = 180 - angle
        if neg:
            angle = -angle
        self.vue_dir = angle

    def set_sneaking(self, value: bool):
        self.sneaking = value
        if self.sneaking:
            self.height = 1.5
        else:
            self.height = 1.9
            self.y += 0.2

    def draw(self, *_, **__):
        assert not _, _
        assert not __, __
        img = self.fragments["front"] if not self.sneaking else self.fragments["sneaking_front"]
        super().draw(img=img)

    def get_mining_speed(self, name_outil):
        if self.game.is_admin:
            return float("inf")

        if name_outil is None:
            return 1
        else:
            return 1

    def jump(self):
        down = self.get_down_block()
        if down is not None:
            if down.collision:
                self.act_speed_y += GRAVITY*20
            elif down.falling_max_speed:
                self.act_speed_y = min(GRAVITY*20, down.falling_max_speed)

    def get_data(self):
        """Retourne les données relatives au joueur"""
        return {
            "x": self.x,
            "y": self.y,
            "life": self.life,
        }

    def set_data(self, data):
        self.life = data["life"]
        self.tp_to(data["x"], data["y"])

    def destroy(self, kill_message: str | None = None):
        self.was_destroyed = True
        self.tp_to(*self.spawnpoint)
        self.life = 100
        if kill_message is not None:
            self.send_death_message(kill_message)

    def send_death_message(self, message: str):
        self.game.chat_manager.send(f"[Death] {message}")

    def event(self, name: str, *args):
        if name == "LIFE_CHANGE":
            # from ..screen_decorators.player_bar.HealthBar import HealthBarManager
            health_manager = self.game.sc_deco.player_bar_manager.health_bar_manager
            health_manager.on_player_life_change()
        else:
            super().event(name, *args)

    kill = destroy


threading.Thread(target=Player.set_img).start()
