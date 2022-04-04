"""
Quelques constantes générales
"""
from enum import IntEnum

HEIGHT_WORLD = 100
HEIGHT_OCEAN = 50

TIME_INCREMENT = 0.2

PLAYER_RANGE = 5

GRAVITY = 0.07

AVERAGE_COLOR_MINDISTANCE = 50

class GameMode(IntEnum):
    SURVIVAL = 0
    CREATIVE = 1
    SPECTATOR = 2
