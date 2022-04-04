"""
PyCraft
By AlphaNow

READ README.md
"""

# Auto install system
import subprocess
from sys import version, stderr

version_name = version.split(" ")[0]
for importname, pipname in [("pygame",)*2, ("requests",)*2, ("yaml", "PyYaml"), ("pyperclip", )*2]:
    try:
        __import__(importname)
    except ImportError:
        subprocess.run(f"py -3.{version_name} -m pip install {pipname}")

# PyGame setup
import pygame
pygame.init()

try:
    import _debug_addons as _
except ImportError:
    pass

# Load the modules / the assets
import code_src

# Launch the game
try:
    code_src.Game()
except KeyboardInterrupt:
    print("Ended with KeyBoardInterrupt", file=stderr)
