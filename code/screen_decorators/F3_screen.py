from .. import Game
from ..utilitaire import PygameText
from ..infos import __version__

SEPARATOR = "------------------"


general_text = f"""
PyCraft Version {__version__}
Created by AlphaNow
{SEPARATOR}
""".removesuffix("\n").removeprefix("\n")

height_char = 15
pad = 2


class F3ScreenManager:
    def __init__(self, game: Game):
        self.game = game
        self.general_text = self.get_pygame_text(general_text)

    def draw(self):
        nb_line = general_text.count("\n") + 1 + pad/height_char
        self.general_text.draw()
        for func_get_info in [self.get_general_info, self.get_block_info, self.get_player_info]:
            text_blocks = func_get_info()
            self.get_pygame_text(text_blocks, y=nb_line*height_char).draw()
            nb_line += text_blocks.count("\n") + 1 + pad/height_char

    def get_block_info(self):
        block_fixed = self.game.map.get_case(*self.game.mouse_pos)
        _n = "\n"
        if block_fixed is None:
            return f"""Block: None\n{SEPARATOR}"""
        else:
            return f"Block: \n{block_fixed.as_str_vue()}\n{SEPARATOR}"

    def get_player_info(self):
        biome = self.game.map.get_biome()
        player = self.game.player
        on_block = self.game.player.get_down_block()
        return f"""
Pos:
    X: {round(player.x, 2)} Y: {round(player.y, 2)}
    On block: {"None" if on_block is None else on_block.name}
    Biome: {biome[0]}
    Temperature: {biome[1]} 
    Humidité: {biome[2]}
UserName: {player.username}
Vue:
    Angle: {round(self.game.player.vue_dir, 2)}
{SEPARATOR}
""".removesuffix("\n").removeprefix("\n")

    def get_general_info(self):
        return f"""
FPS: {round(self.game.clock.get_fps(), 2)}/20
Render Distance: {self.game.zoom}
Gamemode: {self.game.gamemode}
Time: {round(self.game.time)}/360 -> {self.get_time_periode()}
Raining: {self.game.raining}
{SEPARATOR}
""".removesuffix("\n").removeprefix("\n")

    def get_pygame_text(self, text: str, x=0., y=0.) -> PygameText:
        return PygameText(self.game, x, int(y), text=text, alpha=100, height=height_char*(text.count("\n") + 1), pad=pad)

    def get_time_periode(self):
        time = self.game.time
        for periode, end_periode in [("night", 45), ("sunrise", 135), ("day", 225), ("sunset", 315)]:
            if time < end_periode:
                return periode
        return "night"
