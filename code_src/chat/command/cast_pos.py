"""utilisé par certaines commandes"""
from . import token
from ...constants import HEIGHT_WORLD
from .responses import ParamsError
from math import sin, cos, radians, pi


def cast_pos(xy, game, caster=int, y_limitation=True):
    xy = list(xy)
    if any(isinstance(sub, token.RelDirectionPosition) for sub in xy):
        if not all(isinstance(sub, token.RelDirectionPosition) for sub in xy):
            raise ParamsError("if one coord is defined with ^n, all must be")
        dists = xy.copy()
        xy = list(game.player.pos)
        player_angle = radians(game.player.vue_dir)
        if player_angle < 0:
            player_angle = -pi-player_angle
        else:
            player_angle = pi-player_angle
        for (val, angle) in zip(dists, (radians(-90), radians(0))):
            angle += player_angle
            xy[0] += val.value * sin(angle)
            xy[1] += val.value * cos(angle)
    else:
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
