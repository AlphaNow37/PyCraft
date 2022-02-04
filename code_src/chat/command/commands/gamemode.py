from .. import token
from ..responses import Send, ParamsError
from .... import Game
from .. import command


@command.decorate_command(nb_params=0, name="get")
def get_gamemode(game: Game):
    """Commande pour connaitre son mode de jeu"""
    raise Send(f"Gamemode {game.gamemode}", name="Gamemode")


@command.decorate_command(nb_params=1, name="set")
def set_gamemode(new_gamemode, game: Game):
    """Commande pour modifier le son mode de jeu
    set <SURVIVAL-0-s | CREATIVE-1-c | SPECTATOR-2-sp>
    """
    match new_gamemode:
        case str(g) | token.String(g) | token.SpecialString(g) if g.upper() in ("SURVIVAL", "S"):
            gamemode = "SURVIVAL"
        case str(g) | token.String(g) | token.SpecialString(g) if g.upper() in ("CREATIVE", "C"):
            gamemode = "CREATIVE"
        case str(g) | token.String(g) | token.SpecialString(g) if g.upper() in ("SPECTATOR", "SP"):
            gamemode = "SPECTATOR"
        case int(0) | token.Number(0):
            gamemode = "SURVIVAL"
        case int(1) | token.Number(1):
            gamemode = "CREATIVE"
        case int(2) | token.Number(2):
            gamemode = "SPECTATOR"
        case _:
            raise ParamsError("Invalide new gamemode")
    game.change_gamemode(gamemode)


gamemode_help = f"""
Groupe de commande concernant le temps (moment de la journee)

gamemode get: {get_gamemode.help_text}
gamemode set (par defaut): {set_gamemode.help_text}
"""


time_command = command.Command(
    name="gamemode", subcommands=[get_gamemode, set_gamemode], function="set", help_text=gamemode_help
)
command.register_command(time_command)
