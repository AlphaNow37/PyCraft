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

    does_send_death_msg = True

    def set_img(self):
        """Charge le skin du joueur"""
        with open(USER_ROOT / "user.json") as file:
            user_data = json.load(file)
        self.username = user_data["username"]
        skin_dir = CACHE_ROOT / ("skin_" + self.username + ".png")
        if not skin_dir.exists():
            succes = download_skin(skin_dir, self.username)
            if not succes:
                self.game.chat_manager.send(f"Can't load the skin of {self.username}", error=True)
                return False
        base_skin = pygame.image.load(str(skin_dir))
        fragments = self.fragments = get_img_from_skin(base_skin)
        self.fragments = fragments
        self.img = fragments["front"]
        return True

    def __init__(self, game: Game, y):
        super(Player, self).__init__(game, 0, 0)
        self.tp_to(0.5, y)
        self.spawnpoint = [0.5, y]
        self.vue_dir = 0
        self.sneaking = False
        threading.Thread(target=self.set_img).start()

    def move(self, x, y):
        any_ = super().move(x, y)
        self.game.camera_center = (self.x, self.y)
        return any_

    def tick(self):
        self.fall = not self.game.gamemode == "SPECTATOR"
        self.collision = self.fall
        super(Player, self).tick()

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

    def event(self, name: str, *args):
        if name == "LIFE_CHANGE":
            # from ..screen_decorators.player_bar.HealthBar import HealthBarManager
            health_manager = self.game.sc_deco.player_bar_manager.health_bar_manager
            health_manager.on_player_life_change()
        else:
            super().event(name, *args)

    kill = destroy

    @property
    def name(self):
        return self.username


