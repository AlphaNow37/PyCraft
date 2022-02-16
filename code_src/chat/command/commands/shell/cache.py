from . import Game, decorate_command, Command
from .....roots import CACHE_ROOT
from ._clear_dir import clear_dir

@decorate_command(nb_params=0)
def clear_cache(*, game: Game):
    """Commande pour vider le cache"""
    clear_dir(CACHE_ROOT)

clearcache = Command("clearcache", function=clear_cache, )
cache = Command("cache", subcommands={"clear": clear_cache}, help_text=clear_cache.help_text)
