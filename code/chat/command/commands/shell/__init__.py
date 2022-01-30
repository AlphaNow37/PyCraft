from ...command import *
from ...responses import *
from ...token import *
from ..... import Game
from .cache import clearcache, cache
from .saves import clearsaves, saves, del_save
from .user import username, user


shell_help = """
Shell est une commande permattant de gérer les parametres du jeu: cache, username, saves, ...
Mais n'est pas en rapport avec l'instance actuelle du jeu.
/shell dir puis /shell <...> help pour plus d'informations.
"""
subs = [
    clearcache, cache,
    clearsaves, saves, del_save,
    user, username,
]
shell_command = Command("shell", subs, help_text=shell_help)
register_command(shell_command)
