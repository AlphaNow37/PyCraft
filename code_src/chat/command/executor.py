from . import lexer_parser
from . import command as cmd
from . import responses
from ... import Game
from collections.abc import Generator


def execute(input_command: str, game: Game):

    try:
        input_command = input_command.removeprefix("/")
        args = lexer_parser.lex_parse(input_command)
        if not args:
            raise responses.CommandError(f"Invalid command '/{input_command}'")
        res = cmd.root(*args, game=game)
        if isinstance(res, Generator):
            send(next(res), game)
            while True:
                user_input = yield
                to_send = res.send(user_input)
                if to_send is not None:
                    send(to_send, game)
        else:
            responses_exc = []
    except Exception as e:
        responses_exc = [e]
    for e in responses_exc:
        send(e, game)


def send(response_esc, game):
    send = game.chat_manager.send
    try:
        raise response_esc
    except responses.Error as e:
        send(f"[{e.__class__.__name__}] {' '.join(e.args)}", error=True)
    except responses.Send as s:
        send(f"[{s.name}] {' '.join(s.args)}")
    except AssertionError as e:
        error, *args = e.args[0]
        send(f"[{error.__name__}] {' '.join(args)}", error=True)
