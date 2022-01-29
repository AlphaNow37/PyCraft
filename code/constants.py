"""
Quelques constantes générales
"""
import pathlib
ROOT = pathlib.Path(__file__).parent.parent
SRC_ROOT = ROOT / "src"
CACHE_ROOT = ROOT / "cache"
if not CACHE_ROOT.exists():
    CACHE_ROOT.mkdir()

HEIGHT_WORLD = 100
HEIGHT_OCEAN = 50


GAMEMODES = ["CREATIVE", "SURVIVAL", "SPECTATOR"]

TIME_INCREMENT = 0.2

PLAYER_RANGE = 5

GRAVITY = 0.05
