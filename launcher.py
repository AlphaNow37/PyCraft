import subprocess

for name, pipname in [("pygame",)*2, ("requests",)*2, ("yaml", "PyYaml")]:
    try:
        __import__(name)
    except ImportError:
        subprocess.run(f"py -m pip install {pipname}")

import pygame
pygame.init()

import code_src
code_src.Game()

"""
PyCraft
Par AlphaNow

LIRE README.md
"""
