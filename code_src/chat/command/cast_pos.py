"""utilisé par certaines commandes"""
from . import token
from ...constants import HEIGHT_WORLD
from .responses import ParamsError


def cast_pos(xy, game, caster=int, y_limitation=True):
    for i, coord in enumerate(xy):
        match coord:
            case int(coord) | token.Number(coord):
                pass
            case token.RelativePosition(coord_):
                coord = game.player.pos[i] + coord_
                if i == 1:
                    coord -= 1
            case None:
                coord = game.player.pos[i]
                if i == 1:
                    coord -= 1
            case _:
                raise ParamsError("x and y must be numbers")
        xy[i] = coord
    x, y = map(caster, xy)
    if y_limitation and not 0 <= y < HEIGHT_WORLD:
        raise ParamsError(f"y must be in [0->{HEIGHT_WORLD}[")
    return x, y
