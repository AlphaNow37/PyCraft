import random
import pygame
from .. import base_elements, Game
from ..roots import SRC_ROOT
from .skycolor import get_colors
"""S'occupe des nuages"""
CLOUD_ROOT = SRC_ROOT / "environnement" / "clouds"

scaler = 0.1

base_img_height = 38
base_img_width = 76
cloud_height = base_img_height*scaler
cloud_width = base_img_width*scaler

CLOUD = {
    "ALPHA": 160,
    "PERIOD": 50,
    "MIN_Y": 100,
    "MAX_Y": 120,
    "SPEEDS": [0.2, 0.3, 0.5],
    "IMGS": [pygame.image.load(CLOUD_ROOT / name) for name in CLOUD_ROOT.iterdir()],
    "NB_DIVS": 25,
}

block_size = ...
def get_clouds_surface(block_width: block_size, block_height: block_size, resolution, density):
    width, height = int(block_width * resolution), int(block_height * resolution)
    img = pygame.Surface((width, height))
    row_size = CLOUD["PERIOD"] / density
    for index in range(density):
        x = (index * row_size + random.uniform(-row_size / 2, row_size / 2)) % width
        y = random.uniform(CLOUD["MIN_Y"], CLOUD["MAX_Y"]) - CLOUD["MIN_Y"]
        img_cloud = random.choice(CLOUD["IMGS"])
        img_resized = pygame.transform.scale(img_cloud, (cloud_width * resolution, cloud_height * resolution))
        img.blit(img_resized, (x * resolution, y * resolution))
        img.blit(img_resized, (x * resolution - width, y * resolution))
    img.set_alpha(CLOUD["ALPHA"])
    img.set_colorkey("black")
    surface_row_width = width / CLOUD["NB_DIVS"]
    subsurfaces = [img.subsurface([int(surface_row_width * x), 0, surface_row_width, height]) for x in
                   range(CLOUD["NB_DIVS"])]
    return subsurfaces

class CloudSubLayer(base_elements.BaseCarre):
    speed = 0

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.masks = [pygame.mask.from_surface(surface) for surface in self.imgs]

    def tick(self):
        self.x += self.speed
        self.x %= CLOUD["PERIOD"]

    def draw(self, x_self=None, y_self=None, img=None, width=None, height=None, frame=None):
        img = self.imgs[frame]
        mask = self.masks[frame]
        _, mask_rgb = get_colors(int(self.game.time))
        mask_img = mask.to_surface(setcolor=mask_rgb, unsetcolor=(0, 0, 0, 0))
        mask_img.set_alpha(100)
        new_img = img.copy()
        new_img.blit(mask_img, (0, 0))

        super().draw(x_self, y_self, new_img, width, height)


class CloudManager:
    width_layer = CLOUD["PERIOD"]
    width_sublayer = width_layer // CLOUD["NB_DIVS"]
    height_layer = CLOUD["MAX_Y"] - CLOUD["MIN_Y"] + cloud_height

    def __init__(self, game):
        self.game: Game = game
        self.create_clouds()

    def create_clouds(self):
        self.subs = []
        for speed in CLOUD["SPEEDS"]:
            speed_subs = []
            surfaces1 = get_clouds_surface(self.width_layer, self.height_layer, 5, 5)
            surfaces2 = get_clouds_surface(self.width_layer, self.height_layer, 5, 16)
            for surface1, surface2 in zip(surfaces1, surfaces2):
                sublayer = CloudSubLayer(self.game,
                                         imgs=[surface1, surface2], x=0, y=CLOUD["MIN_Y"],
                                         speed=speed,
                                         width=self.width_sublayer, height=self.height_layer)
                speed_subs.append(sublayer)
            self.subs.append(speed_subs)

    def draw(self):
        x_cam, y_cam = self.game.camera_center
        zoom = self.game.zoom
        zoom -= zoom % self.width_sublayer
        zoom += self.width_sublayer
        frame = int(self.game.raining)
        if not (CLOUD["MIN_Y"] > y_cam+zoom or CLOUD["MAX_Y"] < y_cam-zoom):
            for speed_list in self.subs:
                for x_ in range(-zoom-self.width_sublayer*(CLOUD["NB_DIVS"]-1), zoom, self.width_sublayer):
                    sublayer_id = (x_ // self.width_sublayer) % CLOUD["NB_DIVS"]
                    sublayer = speed_list[sublayer_id]
                    x = x_cam + x_ + sublayer.x
                    if x_cam + zoom > x > x_cam - zoom - self.width_sublayer:
                        sublayer.draw(x_self=x, frame=frame)

    def tick(self):
        for speed_list in self.subs:
            for sublayer in speed_list:
                sublayer.tick()
