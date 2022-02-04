from .. import token
from ..responses import Send, ParamsError
from .... import Game
from .. import command


@command.decorate_command(name="set", nb_params=1)
def set_life(raw_life, *, game: Game):
    """Commande pour changer la santé du joueur
    set <number|pourcentage>
    """
    match raw_life:
        case int(int_life):
            new_life = int_life * 5
        case token.Percent(percent):
            new_life = int(percent)
        case float(float_life) | token.Number(float_life):
            new_life = int(float_life * 5)
        case _:
            raise ParamsError("New life must be a number")
    game.player.life = new_life
    raise Send(f"New life is {new_life}/100", name="Life")


@command.decorate_command(name="get", nb_params=0)
def get_life(*, game: Game):
    """Commande pour connaitre la vie du joueur"""
    raise Send(f"The player's life is {game.player.life}/100 = {game.player.life/5} hearths")


@command.decorate_command(name="heal", nb_params=(0, 1))
def heal(raw_value=None, *, game: Game):
    """Commande pour ajouter de la vie au joueur
    heal <number|pourcentage> -> ajoute de la vie
    heal -> redonne l'entiereté de sa vie au joueur
    """
    match raw_value:
        case token.Percent(value):
            game.player.life += int(value)
        case int(value) | token.Number(value) | float(value):
            game.player.life += int(value) * 5
        case None:
            game.player.life = 100
        case _:
            raise ParamsError("Heal must be a number")
    raise Send(f"New life is {game.player.life}/100", name="Life")


life_help = f"""
Groupe de commandes permettant de gerer la vie du joueur

life get (par defaut): {get_life.help_text}
life set: {set_life.help_text}
life heal: {heal.help_text}
"""

life_command = command.Command("life", [set_life, get_life, heal], "get", help_text=life_help)
command.register_command(life_command)
