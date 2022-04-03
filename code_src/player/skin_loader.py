import requests
import base64
import json
from urllib import request
import sys

import pygame


def download_skin(skin_dir, username):
    """Download the skin and return False if there is an error, True otherwith"""
    try:
        resp_to_get_uuid = requests.get(f"https://api.mojang.com/users/profiles/minecraft/{username}")
        uuid = resp_to_get_uuid.json()["id"]
        resp_to_get_skin = requests.get(f"https://sessionserver.mojang.com/session/minecraft/profile/{uuid}")
        value_encoded = resp_to_get_skin.json()["properties"][0]["value"]
        value_decoded = base64.b64decode(value_encoded, )
        url_skin = json.loads(value_decoded.decode())["textures"]["SKIN"]["url"]
        request.urlretrieve(url_skin, skin_dir)
        return True
    except Exception as e:
        print("Erreur dans le chargement du skin :\n", str(e), file=sys.stderr)
        return False


def get_img_from_skin(skin: pygame.Surface) -> dict:
    """transform a minecraft skin into a PyCraft player surface"""
    skin.set_alpha(255)
    # Creating fragments
    names_fragments: dict[str, list[list[int], int]] = {
        "head":
            [[8, 8, 8, 8],
             [40, 8, 8, 8],
             8],

        "body":
            [[20, 20, 8, 12],
             [20, 20, 8, 12],
             4],

        "left_leg":
            [[4, 20, 4, 12],
             [4, 36, 4, 12],
             4],

        "right_leg":
            [[20, 52, 4, 12],
             [4, 52, 4, 12],
             4],

        "left_arm":
            [[44, 20, 4, 12],
             [44, 36, 4, 12],
             4],

        "right_arm":
            [[36, 52, 4, 12],
             [52, 52, 4, 12],
             4],
    }
    fragments: dict[str, dict[str, pygame.Surface] | pygame.Surface] = {}
    for name, sides in names_fragments.items():
        fragments[name] = frag = {}
        surface_1_rect, surface_2_rect, width_side = sides
        x_front_1, y_front_1 = surface_1_rect[:2]
        x_front_2, y_front_2 = surface_2_rect[:2]
        width, height = surface_1_rect[2: 4]
        for side_name, x, width_morceau in [("front", 0, width), ("left", -width_side, width_side), ("right", width, width_side)]:
            frag[side_name] = pygame.Surface((width_morceau, height))
            frag[side_name].blit(skin.subsurface([x_front_1+x, y_front_1, width_morceau, height]), (0, 0))
            frag[side_name].blit(skin.subsurface([x_front_2+x, y_front_2, width_morceau, height]), (0, 0))
    fragments["cou"] = {
        "front": fragments["body"]["front"].subsurface([2, 0, 4, 1]),
        "left": fragments["body"]["left"].subsurface([1, 0, 2, 1]),
        "right": fragments["body"]["right"].subsurface([1, 0, 2, 1]),
    }

    # Creating Front skin
    emplacements_front_skin = {
        #"head": (4, 0),
        "body": (4, 9),
        "cou": (6, 8),
        "left_leg": (4, 21),
        "right_leg": (8, 21),
        "left_arm": (0, 9),
        "right_arm": (12, 9)
    }
    front_skin = pygame.Surface((16, 33))
    front_skin.fill((0, 0, 1))
    front_skin.set_colorkey((0, 0, 1, 0), )
    for name, to in emplacements_front_skin.items():
        front_skin.blit(fragments[name]["front"], to)
    fragments["front"] = front_skin

    # Creating Sneaking Front skin
    sneaking_img = pygame.Surface((front_skin.get_width(), 12 * 3 + 21 * 2))
    sneaking_img.fill((0, 0, 1))
    sneaking_img.set_colorkey((0, 0, 1, 0))
    for x in range(front_skin.get_width()):
        for y in range(front_skin.get_height() - 21):
            for y_inc in range(3):
                sneaking_img.set_at((x, 42 + y * 3 + y_inc), front_skin.get_at((x, 21 + y)))
    for x in range(front_skin.get_width()):
        for y in range(21):
            for y_inc in range(2):
                sneaking_img.set_at((x, y * 2 + y_inc), front_skin.get_at((x, y)))
    fragments["sneaking_front"] = sneaking_img

    # Creating the head scroller
    fragments["head_scroller"] = head_scroller = pygame.Surface((16, 8))
    head_scroller.fill((0, 0, 1))
    head_scroller.set_colorkey((0, 0, 1, 0))
    head_scroller.blit(skin.subsurface([4, 8, 16, 8]), (0, 0))
    head_scroller.blit(skin.subsurface([36, 8, 16, 8]), (0, 0))

    return fragments
