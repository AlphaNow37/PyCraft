import pygame
from .entity import BaseEntity
import math
from .constants import SRC_ROOT, CACHE_ROOT

import requests
import base64
import json
from urllib import request
import sys
import threading

from typing import Union


def download_skin():
    try:
        resp_to_get_uuid = requests.get(f"https://api.mojang.com/users/profiles/minecraft/{USER_NAME}")
        uuid = resp_to_get_uuid.json()["id"]
        resp_to_get_skin = requests.get(f"https://sessionserver.mojang.com/session/minecraft/profile/{uuid}")
        value_encoded = resp_to_get_skin.json()["properties"][0]["value"]
        value_decoded = base64.b64decode(value_encoded, )
        url_skin = json.loads(value_decoded.decode())["textures"]["SKIN"]["url"]
        request.urlretrieve(url_skin, skin_dir)
        return True
    except Exception as e:
        print("Erreur dans le chargement du skin :\n", str(e), file=sys.stderr)
        return False


def get_img_from_skin(skin: pygame.Surface) -> dict:
    # Creating fragments
    names_fragments: dict[str, list[list[int], int]] = {
        "head":
            [[8, 8, 8, 8],
             [40, 8, 8, 8],
             8],

        "body":
            [[20, 20, 8, 12],
             [20, 20, 8, 12],
             4],

        "left_leg":
            [[4, 20, 4, 12],
             [4, 36, 4, 12],
             4],

        "right_leg":
            [[20, 52, 4, 12],
             [4, 52, 4, 12],
             4],

        "left_arm":
            [[44, 20, 4, 12],
             [44, 36, 4, 12],
             4],

        "right_arm":
            [[36, 52, 4, 12],
             [52, 52, 4, 12],
             4],
    }
    fragments: dict[str, Union[dict[str, pygame.Surface], pygame.Surface]] = {}
    for name, cotes in names_fragments.items():
        fragments[name] = frag = {}
        surface_1_rect, surface_2_rect, width_cote = cotes
        x_front_1, y_front_1 = surface_1_rect[:2]
        x_front_2, y_front_2 = surface_2_rect[:2]
        width, height = surface_1_rect[2: 4]
        for name_cote, x, width_morceau in [("front", 0, width), ("left", -width_cote, width_cote), ("right", width, width_cote)]:
            frag[name_cote] = pygame.Surface((width_morceau, height))
            frag[name_cote].blit(skin.subsurface([x_front_1+x, y_front_1, width_morceau, height]), (0, 0))
            frag[name_cote].blit(skin.subsurface([x_front_2+x, y_front_2, width_morceau, height]), (0, 0))
    fragments["cou"] = {
        "front": fragments["body"]["front"].subsurface([2, 0, 4, 1]),
        "left": fragments["body"]["left"].subsurface([1, 0, 2, 1]),
        "right": fragments["body"]["right"].subsurface([1, 0, 2, 1]),
    }

    # Creating Front skin
    emplacements_front_skin = {
        "head": (4, 0),
        "body": (4, 9),
        "cou": (6, 8),
        "left_leg": (4, 21),
        "right_leg": (8, 21),
        "left_arm": (0, 9),
        "right_arm": (12, 9)
    }
    front_skin = pygame.Surface((16, 33))
    front_skin.fill((0, 0, 1))
    front_skin.set_colorkey((0, 0, 1, 0), )
    for name, to in emplacements_front_skin.items():
        front_skin.blit(fragments[name]["front"], to)
    fragments["front"] = front_skin

    # Creating Sneaking Front skin
    sneaking_img = pygame.Surface((front_skin.get_width(), 12 * 3 + 21 * 2))
    sneaking_img.fill((0, 0, 1))
    sneaking_img.set_colorkey((0, 0, 1, 0))
    for x in range(front_skin.get_width()):
        for y in range(front_skin.get_height() - 21):
            for y_inc in range(3):
                sneaking_img.set_at((x, 42 + y * 3 + y_inc), front_skin.get_at((x, 21 + y)))
    for x in range(front_skin.get_width()):
        for y in range(21):
            for y_inc in range(2):
                sneaking_img.set_at((x, y * 2 + y_inc), front_skin.get_at((x, y)))
    fragments["sneaking_front"] = sneaking_img

    # Creating the left of the player
    left = pygame.Surface((8, 32))
    left.blit(fragments["head"]["left"], (0, 0))
    left.blit(fragments["body"]["left"], (1, 8))
    left.blit(fragments["body"]["left"], (1, 20))
    fragments["left"] = left
    fragments["left"] = fragments["body"]["left"]

    return fragments


USER_NAME = "Alpha_Now"
skin_dir = CACHE_ROOT / ("skin_" + USER_NAME + ".png")


class Player(BaseEntity):
    username = USER_NAME
    fragments: dict[str, Union[dict[str, pygame.Surface], pygame.Surface]]
    fragments = get_img_from_skin(pygame.image.load(SRC_ROOT / "entity" / "player.png"))

    height = 1.9
    width = height / fragments["front"].get_height() * fragments["front"].get_width()
    img = fragments["front"]

    @classmethod
    def set_img(cls):
        if not skin_dir.exists():
            succes = download_skin()
            if not succes:
                return
        base_skin = pygame.image.load(skin_dir)
        fragments = cls.fragments = get_img_from_skin(base_skin)
        cls.fragments = fragments
        cls.img = fragments["front"]

    def __init__(self, game, y):
        super(Player, self).__init__(game, 0, 0)
        self.tp_to(0.5, y)
        self.life = 100
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

    def tp_to(self, x, y):
        self.x = x
        self.y = y - self.height / 4 + 1

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
        if down is not None and down.collision:
            self.act_speed_y += 0.7

    def get_data(self):
        return {
            "x": self.x,
            "y": self.y,
            "life": self.life,
        }

    def set_data(self, data):
        self.life = data["life"]
        self.x = data["x"]
        self.y = data["y"]


threading.Thread(target=Player.set_img).start()
