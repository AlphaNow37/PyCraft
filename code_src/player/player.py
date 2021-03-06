import pygame
from ..entity import Mob
from ..base_elements import RotatedImage
import math
from ..roots import SRC_ROOT, CACHE_ROOT, USER_ROOT
from .skin_loader import get_img_from_skin, download_skin
from .. import Game
from ..constants import GRAVITY, GameMode
from .ia import PlayerIA
from ..font import render_line

import json
import threading

class Player(Mob):
    """Classe auquel appartient uniquement le joueur"""

    # Load default skin
    username = None
    fragments: dict[str, dict[str, pygame.Surface] | pygame.Surface]
    fragments = get_img_from_skin(pygame.image.load(SRC_ROOT / "entity" / "player.png"))
    username_overlay = None

    height = 1.9
    width = height / fragments["front"].get_height() * fragments["front"].get_width()
    img = fragments["front"]

    base_life = 100

    does_send_death_msg = True

    ia_cls = PlayerIA
    ia: PlayerIA

    def set_img(self):
        """Charge le skin du joueur, toujours lancé dans un thread
        :return bool: True si le skin a été chargé, False sinon
        """
        with open(USER_ROOT / "user.json") as file:
            user_data = json.load(file)
        self.username = user_data["username"]
        if self.username is None:
            skin_dir = SRC_ROOT / "entity" / "player.png"
        else:
            self.username_overlay = render_line(self.username, "white", "black")

            skin_dir = CACHE_ROOT / ("skin_" + self.username + ".png")
            if not skin_dir.exists():
                succes = download_skin(skin_dir, self.username)
                if not succes:
                    self.game.chat_manager.send(f"Can't load the skin of {self.username}", textcolor="red")
                    return False
        base_skin = pygame.image.load(skin_dir)
        fragments = self.fragments = get_img_from_skin(base_skin)
        self.fragments = fragments
        self.img = fragments["front"]
        return True

    def __init__(self, game: Game, y):
        super(Player, self).__init__(game, 0, 0)
        self.tp_to(0.5, y)
        self.spawnpoint = [0.5, y]

        self.vue_dir = 0
        self.mouse_player_dist = 0

        self.sneaking = False
        threading.Thread(target=self.set_img).start()
        self.head_subnodule = RotatedImage(game, 0, 0.7, width=0.5, height=0.5)

    def move(self, x, y):
        any_ = super().move(x, y)
        self.game.camera_center = (self.x, self.y)
        return any_

    def tick(self):
        self.fall = not self.game.gamemode == GameMode.SPECTATOR
        self.collision = self.fall
        super(Player, self).tick()

    def tp_to(self, x, y):
        self.x = x
        self.y = y - self.height / 4 + 1
        self.game.camera_center = (self.x, self.y)

    def get_distance(self, x, y):
        return math.dist((self.x, self.y), (x, y))

    def update_vue_dir_and_mouse_dist(self):
        w, h = self.game.size_screen
        x1 = w/2
        y1 = h/2
        y1 -= self.head_subnodule.y * self.game.size_block
        x2, y2 = pygame.mouse.get_pos()
        if math.dist((x1, y1), (x2, y2)) < self.head_subnodule.width*2*self.game.size_block:
            self.mouse_player_dist = None
        else:
            self.mouse_player_dist = math.dist((0, 0), (abs(x2 - x1)/w*2, abs(y2 - y1)/h*2)) * 1.2
            self.mouse_player_dist = min(1, self.mouse_player_dist)
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
            self.height = 1.45
        else:
            self.height = 1.9
            self.y += 0.2

    def draw(self, *_, **__):
        assert not _, _
        assert not __, __

        # draw the body
        img = self.fragments["front"] if not self.sneaking else self.fragments["sneaking_front"]
        super().draw(img=img)

        # draw the username overlay
        if self.username_overlay is not None:
            y = self.game.size_screen[1]/2 - self.head_subnodule.height * self.game.size_block * 3
            height = 0.25 * self.game.size_block
            width = height * self.username_overlay.get_width() / self.username_overlay.get_height()
            resized_overlay = pygame.transform.scale(self.username_overlay, (int(width), int(height)))
            self.screen.blit(resized_overlay, (self.game.size_screen[0]/2 - width/2, y))

        # draw the head
        head_x = self.x+self.head_subnodule.x
        head_y = self.y+self.head_subnodule.y
        if self.mouse_player_dist is None:
            self.head_subnodule.draw(img=self.fragments["head"]["front"], angle=0, x_self=head_x, y_self=head_y)
            return
        angle = self.vue_dir
        face_on_right = angle > 0
        face_on_bottom = abs(angle) < 90
        if abs(angle) < 35:
            direction = "vertical"
        elif abs(angle) > 155:
            angle -= 180
            direction = "vertical"
        else:
            angle = angle + (-90 if face_on_right else -270)
            direction = "horizontal"
        scroller = self.fragments["head_scroller"][direction]
        if direction == "horizontal":
            phase = self.mouse_player_dist * 4 * (-1 if face_on_right else 1)
            img = scroller.subsurface([4+phase, 0, 8, 8])
        else:
            phase = self.mouse_player_dist * 2 * (-1 if face_on_bottom else 1)
            img = scroller.subsurface([0, 2 + phase, 8, 8])
        self.head_subnodule.draw(img=img, angle=angle, x_self=head_x, y_self=head_y)

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
