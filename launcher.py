"""
PyCraft
Par AlphaNow

LIRE README.md
"""
import subprocess
from sys import version_info, stderr


for name, pipname in [("pygame",)*2, ("requests",)*2, ("yaml", "PyYaml"), ("pyperclip", )*2]:
    try:
        __import__(name)
    except ImportError:
        subprocess.run(f"py -3.{version_info.minor} -m pip install {pipname}")

import pygame
pygame.init()

try:
    import _debug_addons as _
except ImportError:
    pass

import code_src
try:
    code_src.Game()
except KeyboardInterrupt:
    print("Ended with KeyBoardInterrupt", file=stderr)
