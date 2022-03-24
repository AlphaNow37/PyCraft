import colour

_colors = {
    "black": "000000",
    "dark_blue": "0000AA",
    "dark_green": "00AA00",
    "dark_aqua": "00AAAA",
    "dark_red": "AA0000",
    "dark_purple": "AA00AA",
    "gold": "FFAA00",
    "gray": "AAAAAA",
    "dark_gray": "555555",
    "blue": "55FFFF",
    "green": "55ff55",
    "aqua": "55FFFF",
    "red": "FF5555",
    "light_purple": "FF55FF",
    "yellow": "FFFF55",
    "white": "FFFFFF",
}

id_to_hex = {hex(i)[2]: value for (i, value) in enumerate(_colors.values())}
_name_to_id = {name: hex(i)[2] for (i, name) in enumerate(_colors)}


def get_color_from_name(name):
    if val := _name_to_id.get(name.lower()):
        return "§#" + id_to_hex[val]
    elif val := colour.COLOR_NAME_TO_RGB.get(name.lower()):
        return "§" + colour.rgb2hex((c / 255 for c in val), force_long=True)
    raise ValueError(f"{name!r} is an invalid color")

class _ColorConverter:
    # Used for text=f"abc{clr:blue}def
    def __format__(self, format_spec: str):
        return get_color_from_name(format_spec)
clr = _ColorConverter()

if __name__ == '__main__':
    print(f"Abc{clr:blue}def")
