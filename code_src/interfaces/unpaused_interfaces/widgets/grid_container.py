import pygame
from . import Widget
from ....container import Container


class GridContainer(Widget):
    def __init__(self, game, container, nb_columns, x, y, inter_case_space, case_width):
        super().__init__(game)
        self.container: Container | None = container
        self.nb_columns = nb_columns
        self.x = x
        self.y = y
        self.inter_space = inter_case_space
        self.case_width = case_width

    def draw(self, surface, container=None):
        if container is None:
            container = self.container
        for i, case in enumerate(container):
            y_coord, x_coord = divmod(i, self.nb_columns)
            x = self.x + x_coord * (self.case_width + self.inter_space)
            y = self.y + y_coord * (self.case_width + self.inter_space)
            if case is None:
                # pygame.draw.rect(surface, "red", [x, y, self.case_width, self.case_width])
                pass
            else:
                img = pygame.transform.scale(case.get_img(), (self.case_width+3, self.case_width))
                surface.blit(img, (x, y))
