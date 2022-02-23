from ..command import register_command, decorate_command
from ..responses import Send


@register_command
@decorate_command()
def test(game):
    a = yield Send("Entering ...")
    while a != "quit":
        print(a, "/")
        a = yield Send(f"test {a}")
    raise Send("exited")
