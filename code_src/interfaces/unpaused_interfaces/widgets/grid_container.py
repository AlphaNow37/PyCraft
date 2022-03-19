import pygame
from . import Widget
from ....container import Container, ContainerFragment

_SHOW_RED = False  # for debugging

class GridContainer(Widget):
    # Updated with self.__dict__.update(kwargs)
    can_pose_items = True
    ephemeral_container = False

    def __init__(self, game, container, nb_columns, x, y, inter_case_space, case_width, **kwargs):
        super().__init__(game)
        self.container: Container | ContainerFragment | None = container
        self.nb_columns = nb_columns
        self.x = x
        self.y = y
        self.inter_space = inter_case_space
        self.case_width = case_width

        self.__dict__.update(kwargs)

    def draw(self, surface):
        for i, case in enumerate(self.container):
            y_coord, x_coord = divmod(i, self.nb_columns)
            x = self.x + x_coord * (self.case_width + self.inter_space)
            y = self.y + y_coord * (self.case_width + self.inter_space)
            if case is None:
                if _SHOW_RED:
                    pygame.draw.rect(surface, "red", [x, y, self.case_width, self.case_width])
            else:
                img = pygame.transform.scale(case.get_img(), (self.case_width+3, self.case_width))
                surface.blit(img, (x, y))

    def get_xy_from_rawpos(self, raw_x, raw_y) -> int | None:
        raw_x -= self.x
        raw_y -= self.y
        if raw_x < 0 or raw_y < 0:
            return None
        raw_x /= (self.case_width + self.inter_space)
        raw_y /= (self.case_width + self.inter_space)
        x = int(raw_x)
        y = int(raw_y)
        i = x + y * self.nb_columns
        if i >= len(self.container):
            return None
        return i
