import json
import pygame
from functools import cache
import math


def load_animation(path: str) -> tuple[list[pygame.Surface], int]:
    meta: dict = json.loads(path+".pcmeta")
    meta_animation: dict = meta["animation"]
    frame_time = meta_animation.get("frametime", 1)
    frames_index = meta_animation.get("frames")

    surface = pygame.image.load(path)
    width, height = surface.get_size()
    if frames_index is not None:
        assert height/width == len(frames_index)

    frames = [
        surface.subsurface([0, y*width, width, height])
        for y in range(height//width)
              ]
    if frames_index is not None:
        frames_not_sorted = frames
        frames = [frames_not_sorted[index] for index in frames_index]

    return frames, frame_time


@cache
def get_multiplier_from_angle(angle: int):
    if isinstance(angle, int) and angle <= 45:
        angle = math.radians(angle)
        return math.sin(angle) + math.cos(angle)
    else:
        angle = int(angle)
        angle %= 90
        if angle > 45:
            angle = 90-angle
        return get_multiplier_from_angle(angle)
