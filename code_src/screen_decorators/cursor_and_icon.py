import pygame
from .player_bar.icons import cursor_surface
from ..roots import SRC_ROOT

CURSOR_SIZE = (30, 30)

cursor = pygame.transform.scale(cursor_surface, CURSOR_SIZE)
pygame.mouse.set_cursor(pygame.cursors.Cursor((cursor.get_width()//2, cursor.get_height()//2), cursor))


icon_surface = pygame.image.load(SRC_ROOT / "icon.png")
pygame.display.set_icon(icon_surface)
