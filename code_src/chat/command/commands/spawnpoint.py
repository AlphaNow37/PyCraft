from ..command import register_command, Command, decorate_command
from ..token import Number
from ..responses import Send, ParamsError
from .... import Game
from ..cast_pos import cast_pos


@decorate_command(name="set", nb_params={0, 2})
def set_spawnpoint(x=None, y=None, *, game: Game):
    """Commande pour changer le point de réapparition du joueur
    set <x> <y> -> change le poit vers (x;y)
    set -> change le point vers la position du joueur"""
    player = game.player
    if x is y is None:
        x, y = player.pos
        y -= 1
        y += player.height / 4
        player.spawnpoint = (x, y)
        return
    x, y = cast_pos([x, y], game, caster=int)
    player.spawnpoint = (x+0.5, y+player.height/4)
    raise Send(f"The new spawnpoint is {x=} {y=}", name="Spawnpoint")

@decorate_command(name="get", nb_params=0)
def get_spawnpoint(*, game: Game):
    x, y = game.player.spawnpoint
    """Commande pour voir le point de réapparition du joueur"""
    x -= 0.5
    raise Send(f"The spawnpoint is {x=} {y=}")

help_spawnpoint = f"""
Groupe de commande autour du point de réapparition
spawnpoint set (par defaut): {set_spawnpoint.help_text}
spawnpoint get: {get_spawnpoint.help_text}
"""
spawnpoint_command = Command("spawnpoint", [set_spawnpoint, get_spawnpoint], "set", help_text=help_spawnpoint)
register_command(spawnpoint_command)
