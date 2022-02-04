from ..constants import HEIGHT_OCEAN


def get_height_snow_by_temp(temp: int):
    if temp <= -2:
        height_snow = HEIGHT_OCEAN
    elif temp < 2:
        height_snow = HEIGHT_OCEAN * 1.3
    else:
        height_snow = HEIGHT_OCEAN * 1.9
    return height_snow
