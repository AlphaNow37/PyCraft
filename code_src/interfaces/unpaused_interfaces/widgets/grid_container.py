from . import Widget
from ....container import Container


class GridContainer(Widget):
    def __init__(self, game, container, width):
        super().__init__(game)
        self.container: Container = container
        self.width = width

