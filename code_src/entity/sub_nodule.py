from ..base_elements import BaseImageCentree
from ..tools import get_multiplier_from_angle

import pygame


class SubNodule(BaseImageCentree):
    """
    A sub-nodule is a surface that can to be rotated around its center.
    It it used to create part of an entity, as player head.
    """
    def __init__(self, game, image, rel_x, rel_y, width, height, superentitie, angle=0, **kwargs):
        super().__init__(game, 0, 0, **kwargs)
        self.img = image
        self.rel_x = rel_x
        self.rel_y = rel_y
        self.width = width
        self.height = height
        self.superentitie = superentitie
        self.angle = angle

    def draw(self, x_self=None, y_self=None, img=None, width=None, height=None, frame=None, angle=None):
        assert frame is None, "Not implemented"
        img: pygame.Surface = self.img if img is None else img
        width = self.width if width is None else width
        height = self.height if height is None else height
        rel_x = x_self if x_self is not None else self.rel_x
        rel_y = y_self if y_self is not None else self.rel_y
        angle = self.angle if angle is None else angle
        x = self.superentitie.x + rel_x
        y = self.superentitie.y + rel_y
        multpilier = get_multiplier_from_angle(angle)
        img.set_colorkey((0, 0, 0))
        img = pygame.transform.scale(img, (int(img.get_width()*10), int(img.get_height()*10)))
        rotated_image = pygame.transform.rotate(img, angle)
        width *= multpilier
        height *= multpilier

        super().draw(x, y, rotated_image, width, height)
