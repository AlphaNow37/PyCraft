from . import Game, decorate_command, Command, ParamsError, String
from ._clear_dir import clear_dir
from ..... import roots

@decorate_command(nb_params=0)
def clear_saves(*, game: Game):
    """Commande pour supprimer toutes les parties enregistrées"""
    clear_dir(roots.SAVE_ROOT)

@decorate_command(nb_params=1)
def del_save(name, *, game: Game):
    """Commande pour supprimer une partie enregistrée"""
    match name:
        case String(name) | str(name):
            path = roots.SAVE_ROOT / name
            clear_dir(path)
            path.rmdir()
        case _:
            raise ParamsError("Name must be a string")

clearsaves = Command("clearsaves", function=clear_saves, )
delsave = Command("delsave", function=del_save)
saves = Command("saves", subcommands={"clear": clear_saves, "del": del_save})
