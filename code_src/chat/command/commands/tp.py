from ..responses import ParamsError, Send
from ..command import with_register, decorate_command
from .. import cast_pos
from .... import Game

@with_register(name="teleport")
@with_register(name="tp")
@decorate_command(nb_params=2)
def tp(x, y, *, game: Game):
    """Teleporte le joueur en (x; y)
    /tp <x> <y>"""
    player = game.player
    x, y = cast_pos.cast_pos([x, y], game)
    player.tp_to(x-0.5, y+player.height/4)
    raise Send(f"The player has been teleported to {x=} {y=}", name="Tp")
