from . import Game, decorate_command, Command, OneValueToken, ParamsError
import json
import threading
from .....roots import USER_ROOT
user_path = USER_ROOT / "user.json"

@decorate_command(nb_params=1)
def set_username(new_name, *, game: Game):
    if isinstance(new_name, OneValueToken):
        new_name = new_name.base_value
    new_name: str
    with user_path.open("r") as f:
        user_data = json.load(f)
    user_data["username"] = new_name
    with user_path.open("w") as f:
        json.dump(user_data, f)
    threading.Thread(target=game.player.set_img).start()


user = Command("user", subcommands={"name": set_username})
username = Command("username", function=set_username)
