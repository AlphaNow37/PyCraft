
SUNRISE_TIME = 100  # Time beetween the sky color will change
MIDDLE_SUNRISE_TIME = SUNRISE_TIME/2

BEGIN_SUNRISE = 90-MIDDLE_SUNRISE_TIME  # Sunrise = lever du soleil
END_SUNRISE = 90+MIDDLE_SUNRISE_TIME

BEGIN_SUNSET = 270-MIDDLE_SUNRISE_TIME  # Sunset = coucher du soleil
END_SUNSET = 270+MIDDLE_SUNRISE_TIME

DAY_CLOUDCOLOR = (255, 255, 255)
NIGHT_CLOUDCOLOR = (0, 0, 0)

DAY_SKYCOLOR = (90, 210, 240)
NIGHT_SKYCOLOR = (0, 0, 0)


def _get_changing_color(i, color_type):
    if color_type == "cloud":
        daycolor = DAY_CLOUDCOLOR
        nightcolor = NIGHT_CLOUDCOLOR
    else:
        daycolor = DAY_SKYCOLOR
        nightcolor = NIGHT_SKYCOLOR
    return [
        nightcolor[index] + (daycolor[index]-nightcolor[index]) * i // SUNRISE_TIME
        for index in range(3)
    ]


color = tuple[int | float, int | float, int | float]
def get_colors(time: int) -> (color, color):
    if END_SUNRISE <= time <= BEGIN_SUNSET:
        sky_color = DAY_SKYCOLOR
        cloud_color = DAY_CLOUDCOLOR
    elif time < BEGIN_SUNRISE or time > END_SUNSET:
        sky_color = NIGHT_SKYCOLOR
        cloud_color = NIGHT_CLOUDCOLOR
    else:
        if time < 180:
            i = time - BEGIN_SUNRISE
        else:
            i = END_SUNSET - time
        sky_color = _get_changing_color(i, "sky")
        cloud_color = _get_changing_color(i, "cloud")
    return sky_color, cloud_color
