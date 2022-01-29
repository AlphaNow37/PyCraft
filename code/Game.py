import pygame
import json
from . import map
from . import screen_decorators as sc_deco
from .screen_decorators.Property import Property
from .infos import __version__
from .events import EventManager, get_blocks_size
from .entity import EntityManager
from .chat import Chatmanager
from .interfaces import BaseInterface
from .constants import ROOT


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

        self.interface: BaseInterface | None = None

        self.zoom = 4
        self.camera_center = self.player.pos
        self.size_block = get_blocks_size(self.size_screen, self.zoom)

        self.open_f3 = False
        self.open_chat = False

        self.running = True
        self.pause = False

        self.chat_manager = Chatmanager(self)
        self.mouse_pos = (None, None)
        self.run()

    def run(self):
        while self.running:
            if not self.pause:
                self.events()
                self.update()
            self.flip()
            pygame.display.flip()
            self.clock.tick(20)
            fps = self.clock.get_fps()
            if fps < 15:
                # print(f"[FPS] : {fps}")
                pass
            self.tick += 1
            if self.tick % 20 == 0:
                pass
                # self.global_map = self.map.get_global_map()
        pygame.quit()

    def flip(self):
        if self.interface is None:
            self.sc_deco.draw_sun_moon_sky_weather()
            self.map.draw()
            self.sc_deco.draw_overlays()
            self.entity_manager.draw()
            self.player.draw()
            self.sc_deco.draw_clouds()
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
            self.mouse_pos = self.get_pos_from_screenpos(pygame.mouse.get_pos())
            self.player.update_vue_dir()

            self.player.tick()
            self.sc_deco.tick()
            self.entity_manager.tick()

            if self.open_chat:
                self.chat_manager.tick()
        else:
            self.interface.tick()

    def get_pos_from_screenpos(self, screenpos):
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
        if x < 0:
            x = int(x-1)
        else:
            x = int(x)
        if y < 0:
            y = int(y-1)
        else:
            y = int(y)
        return x, y

    def reset_world(self):
        self.map.generate()
        self.player = self.map.player
        self.sc_deco = sc_deco.ScreenDecorator(self)
        self.tick = 0

        self.time = self.sc_deco.time_manager.time  # 0-> 0h, 90-> 6h, 180-> 12h, 270-> 18h

        self.event_manager = EventManager(self)
        self.entity_manager: EntityManager = EntityManager(self)

        w_manager = self.sc_deco.weather_manager
        self.raining: Property = w_manager.raining
        self.next_rain: Property = w_manager.next_rain

        self.change_gamemode("SURVIVAL" if 0 else "SPECTATOR")

    def save_world(self, name="save"):
        path = ROOT / "saves" / name
        if not path.exists():
            path.mkdir(parents=True)
        general_data_path = path / "data.json"
        general_data = json.dumps({
            "tick": self.tick,
            **self.sc_deco.get_data()
        }, indent=4)
        general_data_path.write_text(general_data, "UTF-8")
        world_data_path = path / "world.json"
        world_data_path.write_text(self.map.get_world_data(), "UTF-8")
        print("save")

    def open_world(self, name="save"):
        path = ROOT / "saves" / name
        general_data_path = path / "data.json"
        general_data = json.loads(general_data_path.read_text("UTF-8"))
        self.tick = general_data["tick"]
        self.sc_deco.set_data(general_data)
        world_data_path = path / "world.json"
        world_data = json.loads(world_data_path.read_text("UTF-8"))
        self.map.set_data(world_data)
        print("open")

    def change_gamemode(self, new_gamemode):
        self.gamemode = new_gamemode
        self.is_admin = self.gamemode in ["CREATIVE", "SPECTATOR"]
