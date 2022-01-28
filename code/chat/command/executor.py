from . import lexer_parser
from . import command as cmd
from . import responses
from ... import Game
from collections.abc import Generator


def execute(input_command: str, game: Game):
    send = game.chat_manager.send
    try:
        input_command = input_command.removeprefix("/")
        args = lexer_parser.lex_parse(input_command)
        if not args:
            raise responses.CommandError(f"Invalid command '/{input_command}'")
        res = cmd.root(*args, game=game)
        print(res)
        if isinstance(res, Generator):
            exceptions = res
        else:
            exceptions = []
    except Exception as e:
        exceptions = [e]
    for e in exceptions:
        try:
            raise e
        except responses.Error as e:
            send(f"[{e.__class__.__name__}] {' '.join(e.args)}", error=True)
        except responses.Send as s:
            send(f"[{s.name}] {' '.join(s.args)}")
        except AssertionError as e:
            error, *args = e.args[0]
            send(f"[{error.__name__}] {' '.join(args)}", error=True)
