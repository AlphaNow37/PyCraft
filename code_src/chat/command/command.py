from . import responses
from . import token

tab = " "*4
text_listdir = """
Commandes:
{names}
(use help to have the helps)
""".strip()


def _default_command(*_, **__):
    raise responses.CommandError("You can't call directly this command")

class Command:
    """Classe gerant les commandes"""
    nb_params_min: int
    nb_params_max: int
    nb_params_possible: set

    def __init__(self, name: str = "_default", subcommands=None, function=_default_command,
                 nb_params=(0, float("inf")), help_text: str = None,
                 _rooted=False):
        """
        Crée une commande
        :param name: Le nom de la commande
        :param subcommands: None-> aucunes subcommand;
                            list[Command] | dict["name", Command] -> permet des /command subcommand
        :param function: None-> impossible de faire /command seul;
                         "name"-> /command <==> /command name
                         callable-> appelle la fonction quand on /command
        :param nb_params: set(...)-> le nombre d'argument passé a la commande doit etre dans le set
                          tuple[min, max]-> le nombre doit etre entre min et max
                          int-> le nombre d'arg doit etre égal au nombre
        :param help_text: le text d'aide accompagnant votre commande. Par defaut, fonction.__doc__
        :param _rooted: Si la commande est la commande racine (/)
        """
        if name == "_default":
            name = function.__name__
        if subcommands is None:
            subcommands = {}
        elif isinstance(subcommands, list):
            subcommands = {cmd.name: cmd for cmd in subcommands}
        if help_text is None:
            if callable(function) and function.__doc__ is not None:
                help_text = function.__doc__
            else:
                help_text = "Aucune aide disponible..."
        self.name = name
        self.subs = subcommands
        if isinstance(function, str):
            self.func: callable = subcommands[function]
        elif callable(function):
            self.func: callable = function
        else:
            raise ValueError("Invalid function, must be either str or callable")
        if isinstance(nb_params, set):
            self.nb_params_min = self.nb_params_max = 0
            self.nb_params_possible = nb_params
        elif isinstance(nb_params, tuple):
            self.nb_params_min, self.nb_params_max = nb_params
            self.nb_params_possible = set()
        else:
            assert isinstance(nb_params, int)
            self.nb_params_min = self.nb_params_max = nb_params
            self.nb_params_possible = set()
        self.nb_params_max: int
        self._rooted = _rooted
        self.help_text = help_text.strip()
        self.__doc__ = self.help_text

    def _nbargs_match(self, nb):
        if self.nb_params_possible:
            if nb in self.nb_params_possible:
                return True
            else:
                raise responses.ParamsError(
f"There must be {' or '.join(map(str, self.nb_params_possible))} arguments for the command {self.name}"
                )
        if self._rooted:
            raise responses.CommandError("Bad syntax in command")
        if self.nb_params_max < nb:
            raise responses.ParamsError(f"Too many arguments for the command {self.name}")
        if self.nb_params_min > nb:
            raise responses.ParamsError(f"Missing arguments for the command {self.name}")

    def __call__(self, *func_args, game):
        func = self.func
        match func_args:
            case (token.String(sub_name), *args) if sub_name in self.subs:
                func = self.subs[sub_name]
            case (token.String("help"), ):
                raise responses.Send(self.help_text, name="Help")
            case (token.String("listdir" | "dir"), ):
                if not self.subs:
                    raise responses.CommandError(f"There is no subcommand in the command {self.name}")
                names = f"\n{tab}-".join(self.subs)
                text = text_listdir.format(names=f"{tab}-{names}")
                raise responses.Send(text, name="ListDir")
            case (token.String(sub_name), *_) if func is _default_command:
                if self._rooted:
                    raise responses.CommandError(f"Unkown command: {sub_name}")
                else:
                    raise responses.CommandError(f"Unkown subcommand for command {self.name}: {sub_name}")
            case args:
                self._nbargs_match(len(args))
        return func(*args, game=game)


root = Command("/", _rooted=True)


def register_command(command: Command, name=None):
    root.subs[name or command.name] = command


def decorate_command(*args, **kwargs):
    def wrap(func) -> Command:
        return Command(*args, **kwargs, function=func)
    return wrap


def with_register(name=None):
    def wrap(func):
        register_command(func, name)
        return func
    return wrap
