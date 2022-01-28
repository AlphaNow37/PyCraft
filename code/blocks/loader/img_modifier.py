import pygame


def get_stair_img(img: pygame.Surface):
    img = img.copy()
    img.fill((0, 0, 0, 0), [0, 0, img.get_width()//2, img.get_height()//2])
    return img

def get_slab_img(img: pygame.Surface):
    return img.subsurface([0, img.get_height()//2, img.get_width(), img.get_height()//2])
