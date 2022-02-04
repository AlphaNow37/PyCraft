from .. import token
from ..responses import CommandError, Send
from .... import Game
from .. import command
from functools import partial


weathers = {
    "rain": True,
    "clear": False,
}


@command.decorate_command(nb_params=0, name="get")
def get_weather(game: Game):
    """Commande pour avoir la météo"""
    raise Send(f"It's {'' if game.raining else 'not'} raining. Next rain in {game.next_rain.get()/20} seconds",
               name="Weather")


@command.decorate_command(nb_params=(1, 2))
def set_weather(new_weather, new_next_time=None, *, game: Game):
    """Commande pour modifier la météo
    set <rain|clear|oui|non|...>
    set <rain|clear|oui|non|...> <temps en tick>
    """
    match new_weather:
        case token.BoolValue(new_time_bool) | bool(new_time_bool):
            game.raining.set(new_time_bool)
        case str(new_weather) | token.SpecialString(new_weather) if new_weather in weathers:
            game.raining.set(weathers[new_weather])
        case token.none:
            pass
        case _:
            raise CommandError(f"Invalid new_weather: '{new_weather}'")
    match new_next_time:
        case None | token.none:
            game.next_rain.reset()
        case token.Number(new_next_time) if (new_next_time := int(new_next_time)) > 0:
            game.next_rain.set(new_next_time)
        case _:
            raise CommandError(f"Invalid new_next_time: '{new_next_time}'")
    raise Send(f"It's {'' if game.raining else 'not'} raining. Next rain in {game.next_rain.get()/20} seconds",
               name="Weather")


weather_help = f"""
Groupe de commande concernant la météo

weather get (par defaut): {get_weather.help_text}
weather set: {set_weather.help_text}

weather clear/weather rain -> raccourcis pour weather set
"""


weather_subs = {
    "get": get_weather,
    "set": set_weather,
    "clear": partial(set_weather, False, ),
    "rain": partial(set_weather, True),
}
weather_command = command.Command("weather", weather_subs, "get", help_text=weather_help)
command.register_command(weather_command)
