from ..command import register_command, decorate_command
from ..responses import Send
from .... import Game


@decorate_command(nb_params=0)
def seed(*, game: Game):
    """Commande pour avoir la seed du monde"""
    raise Send(f"The seed is {game.map.seed}", name="Seed")

register_command(seed)
