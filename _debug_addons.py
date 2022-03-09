import pygame
already_show = False
def show(self: pygame.Surface):
    global already_show
    if already_show:
        return
    from PIL import Image
    s = pygame.image.tostring(self, "RGBA")
    Image.frombuffer("RGBA", self.get_size(), s).show()
    already_show = True

setattr(pygame, "show", show)
