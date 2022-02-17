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
    "chat": [pygame.K_t]
}


class KeyMapManager:
    """
    Singleton stockant les touches
    """
    with open("user/key_map.json") as file:
        keys: dict[str, list[int]] = json.load(file)

    @classmethod
    def change_key(cls, name, value):
        if name in reserved_keys:
            raise KeyChangeError()
        for keys in cls.keys.values():
            if value in keys:
                keys.remove(value)
        cls.keys[name].append(value)
        with open("user/key_map.json", "w") as file:
            json.dump(cls.keys, file, indent=4)

    @classmethod
    def reset(cls):
        cls.keys = default_keys
        with open("user/key_map.json", "w") as file:
            json.dump(cls.keys, file, indent=4)

    def __class_getitem__(cls, item):
        return cls.keys[item]

    get = classmethod(__class_getitem__)

    @classmethod
    def is_pressed(cls, pressed, action):
        keys = cls.keys[action]
        if not isinstance(keys, tuple | list):
            keys = (keys, )
        if action == "chat":
            print(keys)
        return any(pressed[key] for key in keys)
