from ..responses import Send, CommandError
from ..command import register_command, decorate_command
from ..token import OneValueToken, SpecialString
from .... import Game

_allow_exec = True

builtins = __builtins__.copy()
builtins["open"] = None
builtins["__import__"] = None
@register_command
@decorate_command(name="exec", nb_params=1)
def exec_command(data, *, game: Game):
    if not _allow_exec:
        raise CommandError("You can't use the exec command because of the settings")
    if isinstance(data, SpecialString):
        to_exec = data.value
        print(to_exec)
    elif isinstance(data, OneValueToken):
        to_exec = data.base_value
    else:
        to_exec = str(data)
    execs_globals = {
        "__builtins__": builtins,
        "player": game.player,
        "game": game,
        "map": game.map,
        "sc_deco": game.sc_deco,
    }
    try:
        try:
            res = eval(to_exec, execs_globals)
            raise Send(f"{res}", name="Exec")
        except SyntaxError:
            exec(to_exec, execs_globals)
    except Exception as e:
        raise CommandError(f"{e}")
