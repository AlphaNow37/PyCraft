import pygame


def get_stair_img(img: pygame.Surface):
    img = img.copy()
    img.fill((0, 0, 0, 0), [img.get_width()//2, 0, img.get_width(), img.get_height()//2])
    return img

def get_slab_img(img: pygame.Surface):
    return img.subsurface([0, 0, img.get_width(), img.get_height()//2])


def cut_img(img: pygame.Surface, nb: int | str):
    width = img.get_width()
    height = img.get_height()
    if nb == "auto":
        nb = height // width
    cutted_height = height // nb
    return [img.subsurface([0, y*cutted_height, width, cutted_height]) for y in range(nb)], nb
