import random
import pygame
from .. import base_elements, Game

CLOUD = {
    "COLOR": "#DDDDDD",
    "ALPHA": 160,
    "PERIOD": 256,
    "PERIOD_SPEED": 0.05,
    "Y": 75,
    "NB": 32,
    "HEIGHT": 3,
    "MAX_SPEED": {
        "Y": 0.1,
        "X": 0.3,
    }
}


class Cloud(base_elements.BaseCarre):
    img = texture_cloud = pygame.Surface((1, 1))
    img.fill(CLOUD["COLOR"])
    alpha = CLOUD["ALPHA"]

    width = CLOUD["PERIOD"]//CLOUD["NB"]//2
    height = CLOUD["HEIGHT"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.y += random.randint(0, 2)
        self.speed_x = 0
        self.speed_y = 0

    def tick(self):
        self.speed_y += random.randint(-5, 5)/500
        self.speed_y = max(min(self.speed_y, CLOUD["MAX_SPEED"]["Y"]), -CLOUD["MAX_SPEED"]["Y"])
        self.y += self.speed_y
        if self.y < CLOUD["Y"]-CLOUD["HEIGHT"]//2:
            self.speed_y = 0.05
        if self.y > CLOUD["Y"]+CLOUD["HEIGHT"]//2:
            self.speed_y = -0.05

        self.speed_x += random.randint(-5, 5) / 400
        self.speed_x = max(min(self.speed_x, CLOUD["MAX_SPEED"]["X"]), -CLOUD["MAX_SPEED"]["X"])
        self.x += self.speed_x
        self.x += CLOUD["PERIOD_SPEED"]
        self.x %= CLOUD["PERIOD"]


class CloudManager:
    def __init__(self, game):
        self.game: Game = game
        self.clouds = [Cloud(game, CLOUD["PERIOD"]//CLOUD["NB"]*x, CLOUD["Y"]) for x in range(CLOUD["NB"])]

    def draw(self):
        x_cam, y_cam = self.game.camera_center
        zoom = self.game.zoom
        if not (CLOUD["Y"]-CLOUD["HEIGHT"] > y_cam+zoom or CLOUD["Y"]+CLOUD["HEIGHT"] < y_cam-zoom):
            left_screen = x_cam-zoom
            left = left_screen
            left -= left % CLOUD["PERIOD"]
            for x in range(zoom*2//CLOUD["PERIOD"]+2):
                left_period = left+x*CLOUD["PERIOD"]
                for cloud in self.clouds:
                    cloud.draw(x_self=left_period+cloud.x)

    def tick(self):
        for cloud in self.clouds:
            cloud.tick()
