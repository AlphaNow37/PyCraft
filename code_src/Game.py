import math
import pygame
import json

from . import map
from .screen_decorators import ScreenDecorator
from .screen_decorators.Property import Property
from .infos import __version__
from .events import EventManager, get_blocks_size
from .entity import EntityGroup
from .chat import Chatmanager
from .interfaces import AbcInterface
from .roots import SAVE_ROOT
from .tests import TestManager
from .sounds import SoundManager


_PROFILING = False
_TESTING = False

"""
Fichier principale aceuillant la classe Game, la racine du jeu
"""

class Game:

    def __init__(self):
        self.size_screen = (1080, 720)

        self.screen = pygame.display.set_mode(self.size_screen, pygame.RESIZABLE)

        pygame.display.set_caption(f"PyCraft {__version__}")
        self.clock = pygame.time.Clock()
        self.map = map.Map(self)

        self.reset_world()

        self.interface: AbcInterface | None = None

        self.zoom = 4
        self.camera_center = self.player.pos
        self.size_block = get_blocks_size(self.size_screen, self.zoom)

        self.open_f3 = False
        self.open_chat = False

        self.running = True
        self.pause = False
        self.mouse_pos = (None, None)
        self.mouse_pos_side = (None, None)

        self.chat_manager = Chatmanager(self)
        self.sound_manager: SoundManager = SoundManager(self)

        if _TESTING:
            self.test_manager = TestManager(self)

        if _PROFILING:
            import cProfile
            profile = cProfile.Profile()
            with profile:
                self.run()
            profile.print_stats(sort="cumtime")
        else:
            self.run()

    def run(self):
        """
        Boucle principale du jeu
        """
        while self.running:
            if not self.pause:
                self.events()
                self.update()
            self.flip()
            pygame.display.flip()
            self.clock.tick(20)
            # fps = self.clock.get_fps()
            # if fps < 15:
            #     print(f"[FPS] : {fps}")
            #     pass
            self.tick += 1
            if self.tick % 20 == 0:
                pass
                # self.global_map = self.map.get_global_map()
            if _TESTING:
                self.test_manager.tick()
        pygame.quit()

    def flip(self):
        """
        Réactualise l'ecran en affichant tout
        """
        if self.interface is None:
            self.sc_deco.draw_sun_moon_sky_weather()
            self.map.draw()
            self.sc_deco.draw_overlays()
            self.entities.draw()
            self.player.draw()
            self.sc_deco.draw_clouds()
            self.sc_deco.draw_bars()
            if self.open_chat:
                self.chat_manager.draw()
            elif self.open_f3:
                self.sc_deco.draw_f3_screen()
        else:
            self.interface.draw()

    def events(self):
        self.event_manager.events()

    def update(self):
        if self.interface is None:
            x, y, side_x, side_y = self.get_pos_from_screenpos(pygame.mouse.get_pos())
            self.mouse_pos = [x, y]
            self.block_side = [side_x, side_y]

            self.player.update_vue_dir()

            self.player.tick()
            self.sc_deco.tick()
            self.entities.tick()
            self.map.tick()
            self.sound_manager.tick()

            if self.open_chat:
                self.chat_manager.tick()
        else:
            self.interface.tick()

    def get_pos_from_screenpos(self, screenpos):
        """
        :param screenpos: (x; y) de la souris sur l'ecran
        :return: (x; y; side-x; side-y) en jeu
        """
        x, y = screenpos
        x_cam, y_cam = self.camera_center
        width, height = self.size_screen
        y = height-y
        x -= width/2
        y -= height/2
        x /= self.size_block
        y /= self.size_block
        x += x_cam
        y += y_cam
        x_block = math.floor(x)
        y_block = math.floor(y)
        return x_block, y_block, x-x_block, y-y_block

    def reset_world(self):
        self.map.generate()
        self.player = self.map.player
        self.sc_deco: ScreenDecorator = ScreenDecorator(self)
        self.tick = 0

        self.time = self.sc_deco.time_manager.time  # 0-> 0h, 90-> 6h, 180-> 12h, 270-> 18h

        self.event_manager = EventManager(self)
        self.entities: EntityGroup = EntityGroup(self)

        w_manager = self.sc_deco.weather_manager
        self.raining: Property = w_manager.raining
        self.next_rain: Property = w_manager.next_rain

        self.change_gamemode("SURVIVAL" if 0 else "SPECTATOR")

    def save_world(self, name="save"):
        if "." in name or "/" in name or "\\" in name:
            raise ValueError(f"Invalid name {name}")
        path = SAVE_ROOT / name
        if not path.exists():
            try:
                path.mkdir()
            except OSError as e:
                if e.winerror == 123:  # Problem with the name of the dir
                    raise ValueError(f"Invalid name {name}")
                else:
                    raise e
        general_data_path = path / "data.json"
        general_data = json.dumps({
            "tick": self.tick,
            **self.sc_deco.get_data()
        }, indent=4)
        general_data_path.write_text(general_data, "UTF-8")
        world_data_path = path / "world.json"
        world_data_path.write_text(self.map.get_world_data(), "UTF-8")
        little_map_data_path = path / "little_map.json"
        little_map_data_path.write_text(json.dumps(self.map.get_little_data(), indent=4), "UTF-8")
        print("save")

    def open_world(self, name="save"):
        path = SAVE_ROOT / name
        if not path.exists():
            raise ValueError(f"The save {name} doesn't exist")
        general_data_path = path / "data.json"
        general_data = json.loads(general_data_path.read_text("UTF-8"))
        self.tick = general_data["tick"]
        self.sc_deco.set_data(general_data)
        world_data_path = path / "world.json"
        world_data = json.loads(world_data_path.read_text("UTF-8"))
        self.map.set_world_data(world_data)
        little_map_data_path = path / "little_map.json"
        little_map_data = json.loads(little_map_data_path.read_text("UTF-8"))
        self.map.set_little_data(little_map_data)
        print("open")

    def change_gamemode(self, new_gamemode):
        self.gamemode = new_gamemode
        self.is_admin = self.gamemode in ["CREATIVE", "SPECTATOR"]

    def test_id(self, test_id):
        assert _TESTING
        self.test_manager.test_id(test_id)
