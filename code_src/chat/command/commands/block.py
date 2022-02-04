from .. import token
from ..responses import Send, ParamsError
from .... import Game
from .. import command
from ....constants import HEIGHT_WORLD
from ....blocks import blocks


_default = object()


def cast_pos(xy, game):
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
    x, y = map(int, xy)
    if y < 0 or y >= HEIGHT_WORLD:
        raise ParamsError(f"y must be in [0->{HEIGHT_WORLD}[")
    return x, y


@command.decorate_command(nb_params={0, 2}, name="get")
def get_block(x=None, y=None, *, game: Game):
    """Commande pour connaitre un block
    get <number|~relative> <number|~relative>"""
    x, y = cast_pos([x, y], game)
    block = game.map.get_case(x, y)
    visu = block.get_visualisation()
    block_infos = blocks.get(block.name, {})
    important_infos = {
        name: value
        for (name, value) in visu.items()
        if block_infos.get(name, _default) != value
    }
    raise Send(f"Block:\n{block.as_str_vue(visu)}\npycraft:{block.name}{important_infos or ''}", name="Block")

@command.with_register(name="setblock")
@command.decorate_command(nb_params={1, 3}, name="set")
def set_block(x, y=None, new_block=None, *, game: Game):
    """Commande pour modifier un block
    get <number|~relative> <number|~relative> <block|block{...}>
    block -> [pycraft:|minecraft:]<name>   ex: glass, minecraft:sand, pycraft:ice"""
    if y is new_block is None:
        new_block, x = x, None
    if not isinstance(new_block, token.Block):
        raise ParamsError(f"Invalid block: {new_block}")
    x, y = cast_pos([x, y], game)
    game.map.set_case(x, y, game.map.get_block_from_resume(new_block.value, x, y))


@command.with_register()
@command.decorate_command(nb_params=(5, float("inf")))
def fill(x1, y1, x2, y2, new_block, *args, game: Game):
    x1, y1 = cast_pos([x1, y1], game)
    x2, y2 = cast_pos([x2, y2], game)
    if not isinstance(new_block, token.Block):
        raise ParamsError(f"Invalid block: {new_block}")
    new_block_value = new_block.value
    block_to_replace = None
    match args:
        case ():
            pass
        case (token.String("replace"), token.Block(block)):
            block_to_replace = game.map.get_block_from_resume(block, None, None).get_visualisation()
        case (token.String("replace"), invalid_block):
            raise ParamsError(f"Invalid replaced block: {invalid_block}")
        case _:
            raise ParamsError(f"Invalid params: {' '.join(map(str, args))}")
    map_ = game.map
    x1, x2 = sorted((x1, x2))
    y1, y2 = sorted((y1, y2))
    for x in range(x1, x2):
        for y in range(y1, y2):
            if block_to_replace is not None:
                block = map_.get_case(x, y)
                if block.get_visualisation() != block_to_replace:
                    continue
            map_.set_case(x, y, map_.get_block_from_resume(new_block_value, x, y))

block_help = f"""
Groupe de commande concernant les blocs

block get (par defaut): {get_block.help_text}
block set: {set_block.help_text}

setblock -> raccourcis pour block set
"""


block_command = command.Command(name="block", subcommands=[get_block, set_block, fill],
                                function="get", help_text=block_help)
command.register_command(block_command)
