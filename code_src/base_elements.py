import pygame
import math

from . import map


class BaseCarre:
    """
    Classe abstraite pour un objet drawable
    """
    font = pygame.font.Font(None, 500)

    img: pygame.Surface = pygame.Surface((1, 1))
    img.fill((100, 0, 100))
    frame = 0
    imgs: list[pygame.Surface] | None = None

    width = 1
    height = 1

    alpha = 255

    flip_x = False
    flip_y = False

    frametime = None

    def __init__(self, game, x, y, **kwargs):
        self.__dict__.update(kwargs)
        self.map: map.Map = game.map
        self.screen: pygame.Surface = game.screen
        self.game = game
        self.x = x
        self.y = y
        if self.frametime:
            self.remaining_frametime = self.frametime

    def draw(self, x_self=None, y_self=None, img=None, width=None, height=None, frame=None):
        if self.frametime:
            self.remaining_frametime -= 1
            if self.remaining_frametime <= 0:
                self.remaining_frametime = self.frametime
                self.frame += 1
                self.frame %= len(self.imgs)

        if x_self is None:
            x_self = self.x
        if y_self is None:
            y_self = self.y
        width_screen, height_screen = self.game.size_screen
        x, y = self.get_screen_position(x_self, y_self)

        if img is None:
            if self.imgs is None:
                img = self.img
            else:
                img = self.imgs[self.frame if frame is None else frame]
        if width is None:
            width = self.width
        if height is None:
            height = self.height
        width *= self.game.size_block
        height *= self.game.size_block
        img = pygame.transform.scale(img, (int(width)+1, int(height)+1))
        if self.flip_x or self.flip_y:
            img = pygame.transform.flip(img, self.flip_x, self.flip_y)
        img.set_alpha(self.alpha)

        y = height_screen - y - height
        self.screen.blit(img, (x, y))

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
        super().draw(x_self-self.width/2, y_self-self.height/2, img, width, height, frame)

    def get_rect(self) -> pygame.Rect:
        return pygame.Rect((self.x-self.width/2)*100, (self.y-self.height/2)*100, self.width*100, self.height*100)

    def get_int_pos(self):
        return [math.ceil(self.x)-1, int(self.y)]
