from ..responses import Send, CommandError, Error
from ..command import register_command, decorate_command
from ..token import OneValueToken, SpecialString
from .... import Game

_allow_exec = True

cancel_worlds = ("quit", "x")
run_worlds = ("", "run", "ok")
specials_worlds = cancel_worlds + run_worlds

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
    elif isinstance(data, OneValueToken):
        to_exec = data.base_value
    else:
        to_exec = str(data)

    to_send = []

    def custom_print(*args, sep=" ", end="\n"):
        text = sep.join(map(str, args)) + end
        to_send.append(text)

    execs_globals = {
        "__builtins__": builtins,
        "player": game.player,
        "game": game,
        "map": game.map,
        "sc_deco": game.sc_deco,
        "print": custom_print,
    }
    if to_exec.strip() == ">":
        to_exec = ""
        line = yield Send("Enter your code, "
                          "\ntype 'quit' or 'X' to cancel, "
                          "\n'run', 'ok' or an empty line to run", name='Exec')
        line = line.strip()
        while line not in specials_worlds:
            to_exec += line
            line = yield
            line = line.strip()

    try:
        try:
            res = eval(to_exec, execs_globals)
            if to_send:
                raise Send(f"\n{''.join(to_send)}\n{res}", name="Exec")
            raise Send(str(res), name="Exec")
        except SyntaxError:
            exec(to_exec, execs_globals)
    except Exception as e:
        if not isinstance(e, (Send, Error)):
            raise CommandError(f"({e.__class__.__name__}){e}")
        else:
            raise e
    else:
        if to_send:
            raise Send(f"\n{''.join(to_send)}", name="Exec")
