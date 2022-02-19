from .. import token
from ..responses import Send, ParamsError
from .... import Game
from .. import command


times = {
            "night": 0,
            "day": 180,
            "sunrise": 90,
            "sunset": 270,
        }


@command.decorate_command(nb_params=0, name="get")
def get_time(game: Game):
    """Commande pour avoir le temps de la journée
    0=minuit 180=midi"""
    raise Send(f"Time={game.time.get():.2f}", name="Time")


@command.decorate_command(nb_params=1, name="set")
def set_time(new_time, game: Game):
    """Commande pour modifier le temps
    set <day|night|sunrise|sunset|number>
    0=minuit 180=midi
    """
    if isinstance(new_time, token.Number):
        new_time = float(new_time)
        assert 0 <= new_time <= 360, (ParamsError, "The new time must be in range 0->360,\n0=night 180=day")
        game.time.set(new_time)
    elif isinstance(new_time, (token.SpecialString, str, token.String)):
        new_time_int = times.get(str(new_time))
        if new_time_int is None:
            raise ParamsError("Invalid time '{}',\ncan be in '{}'"
                              .format(new_time, "', '".join(times)))
        game.time.set(new_time_int)
    else:
        raise ParamsError(f"Invalid data '{str(new_time)}'")
    raise Send(f"Time changed to {new_time}", name="Time")


time_help = f"""
Groupe de commande concernant le temps (moment de la journee)

time get (par defaut): {get_time.help_text}
time set: {set_time.help_text}
"""


time_command = command.Command(name="time", subcommands=[get_time, set_time], function="get", help_text=time_help)
command.register_command(time_command)
