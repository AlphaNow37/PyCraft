import json
import pygame


class KeyChangeError(Exception):
    def __str__(self):
        return "This key is a reserved key"

reserved_keys = [pygame.K_TAB, pygame.K_ESCAPE]
default_keys = {
    "left": [pygame.K_q],
    "right": [pygame.K_d],
    "jump": [pygame.K_SPACE, pygame.K_z],
    "sneak": [pygame.K_LSHIFT, pygame.K_s],
    "chat": [pygame.K_t],
    "inventory": [pygame.K_e],
}


class KeyMapManager:
    """
    Objet gerant les touches
    """
    with open("user/key_map.json") as file:
        keys: dict[str, list[int]] = json.load(file)

    def change_key(self, name, value):
        if name in reserved_keys:
            raise KeyChangeError()
        for keys in self.keys.values():
            if value in keys:
                keys.remove(value)
        self.keys[name].append(value)
        with open("user/key_map.json", "w") as file:
            json.dump(self.keys, file, indent=4)

    def reset(self):
        self.keys = default_keys
        with open("user/key_map.json", "w") as file:
            json.dump(self.keys, file, indent=4)

    def __getitem__(self, item):
        return self.keys[item]

    get = __getitem__

    def is_pressed(self, pressed, action):
        keys = self.keys[action]
        if not isinstance(keys, tuple | list):
            keys = (keys, )
        if action == "chat":
            print(keys)
        return any(pressed[key] for key in keys)
