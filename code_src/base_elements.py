import pygame
import math

from .tools import get_multiplier_from_angle
from . import map
from .constants import AVERAGE_COLOR_MINDISTANCE


class BaseCarre:
    """
    Classe abstraite pour un objet drawable
    """
    font = pygame.font.Font(None, 500)

    img: pygame.Surface = pygame.Surface((1, 1))
    img.fill((100, 0, 100))
    frame = 0
    imgs: list[pygame.Surface] | None = None
    average_color = None  # When the camera is very unzoomed, we don't show the real image is this is not None

    width = 1
    height = 1

    alpha = 255

    flip_x = False
    flip_y = False

    frametime = None
    nb_frames = None

    def __init__(self, game, x, y, **kwargs):
        self.__dict__.update(kwargs)
        self.map: map.Map = game.map
        self.screen: pygame.Surface = game.screen
        self.game = game
        self.x = x
        self.y = y

    def draw(self, x_self=None, y_self=None, img=None, width=None, height=None, frame=None):
        if self.frametime:
            self.frame = (self.game.tick // self.frametime) % self.nb_frames

        if x_self is None:
            x_self = self.x
        if y_self is None:
            y_self = self.y
        width_screen, height_screen = self.game.size_screen
        # x, y = self.get_screen_position(x_self, y_self)

        x_cam, y_cam = self.game.camera_center
        # width_screen, height_screen = self.game.size_screen
        delta_x = x_self - x_cam
        delta_y = y_self - y_cam
        x = self.game.size_block * delta_x + width_screen / 2
        y = self.game.size_block * delta_y + height_screen / 2

        if width is None:
            width = self.width
        if height is None:
            height = self.height
        width *= self.game.size_block
        height *= self.game.size_block
        width = int(width) + 1
        height = int(height) + 1
        y = height_screen - y - height

        if self.game.zoom < AVERAGE_COLOR_MINDISTANCE or self.average_color is None or self.alpha < 255:
            if img is None:
                if self.imgs is None:
                    img = self.img
                else:
                    img = self.imgs[self.frame if frame is None else frame]

            img = pygame.transform.scale(img, (width, height))
            if self.flip_x or self.flip_y:
                img = pygame.transform.flip(img, self.flip_x, self.flip_y)
            img.set_alpha(self.alpha)
            self.screen.blit(img, (x, y))
        else:
            pygame.draw.rect(self.screen, self.average_color, [x, y, width, height])

    def get_rect(self) -> pygame.Rect:
        return pygame.Rect(self.x*100, self.y*100, self.width*100, self.height*100)

    def get_screen_position(self, x, y):
        x_cam, y_cam = self.game.camera_center
        width_screen, height_screen = self.game.size_screen
        x = x - x_cam
        y = y - y_cam
        x *= self.game.size_block
        y *= self.game.size_block
        x += width_screen / 2
        y += height_screen / 2
        return x, y

    @property
    def pos(self):
        return self.x, self.y

    @pos.setter
    def pos(self, value):
        self.x, self.y = value


class BaseImageCentree(BaseCarre):
    """
    Classe abstraite dont les coordonnées sont celle de son centre et pas de son coin
    """

    def draw(self, x_self=None, y_self=None, img=None, width=None, height=None, frame=None):
        if x_self is None:
            x_self = self.x
        if y_self is None:
            y_self = self.y
        width = width if width is not None else self.width
        height = height if height is not None else self.height
        super().draw(x_self-width/2, y_self-height/2, img, width, height, frame)

    def get_rect(self) -> pygame.Rect:
        return pygame.Rect((self.x-self.width/2)*100, (self.y-self.height/2)*100, self.width*100, self.height*100)

    def get_int_pos(self):
        return [math.ceil(self.x)-1, int(self.y)]


class RotatedImage(BaseImageCentree):
    """
    Classe Abstraite pouvant etre rotate
    """
    def __init__(self, game, x, y, angle=0, center=None, do_freeze_img=False, **kwargs):
        super().__init__(game, x, y, **kwargs)
        self.angle = angle
        self.center = center
        if do_freeze_img:  # Faster
            self.img = self.get_centered_img(self.img, self.center)
            self.center = None

    def draw(self, x_self=None, y_self=None, img=None, width=None, height=None, frame=None, angle=None, center=None):
        assert frame is None, "Not implemented"
        img: pygame.Surface = self.img if img is None else img
        width = self.width if width is None else width
        height = self.height if height is None else height
        x = x_self if x_self is not None else self.x
        y = y_self if y_self is not None else self.y
        angle = self.angle if angle is None else angle
        multpilier = get_multiplier_from_angle(angle)
        if not (self.center is center is None):  # Slower
            img = self.get_centered_img(img, center if center is not None else self.center)
        img.set_colorkey((0, 0, 0))
        img = pygame.transform.scale(img, (int(img.get_width()*10), int(img.get_height()*10)))
        rotated_image = pygame.transform.rotate(img, angle)
        width *= multpilier
        height *= multpilier
        super().draw(x, y, rotated_image, width, height)

    @staticmethod
    def get_centered_img(uncentered_img, center):
        x_center, y_center = center
        img_width, img_height = uncentered_img.get_size()
        if x_center * 2 < img_width:
            left = img_width - 2 * x_center
            new_width = 2 * img_width - 2 * x_center
        else:
            left = 0
            new_width = 2 * x_center
        if y_center < img_height / 2:
            top = img_height - 2 * y_center
            new_height = 2 * img_height - 2 * y_center
        else:
            top = 0
            new_height = 2 * y_center
        centered_img = pygame.Surface((new_width, new_height))
        centered_img.blit(uncentered_img, (left, top))
        return centered_img
