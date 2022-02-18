import unittest
from ..player import Player
from ..map import Map
from .. import Game

class TestManager:
    registered_test = []

    def __init__(self, game):
        self.game = game
        self.tests = [cls(game) for cls in self.registered_test]

    def tick(self):
        for test in self.tests:
            test.tick()

    def test_id(self, test_id):
        for test in self.tests:
            for name, value in test.__class__.__dict__.items():
                if callable(value) and name == test_id:
                    value(test)

class Test(unittest.TestCase):
    player: Player
    map: Map
    game: Game

    def __init_subclass__(cls, **kwargs):
        TestManager.registered_test.append(cls)

    def __init__(self, game):
        super().__init__()
        self.game = game
        self.player = game.player
        self.map = game.map

    def tick(self):
        pass

# Auto import all the tests
import pathlib
command_path = pathlib.Path(__file__).parent
files = [path.name for path in command_path.iterdir() if path.name not in ("__pycache__", "__init__")]
__import__("", level=1, fromlist=files, globals=globals())