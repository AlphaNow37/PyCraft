from .blocks import Block
import pygame


class Grass(Block):
    img_snow = pygame.image.load("src/blocks/surface/snow_grass.png")
    img_grass = pygame.image.load("src/blocks/surface/grass.png")

    def draw(self, *args, **kwargs):
        dessus: Block = self.map.get_case(self.x, self.y+1)
        if dessus is not None and dessus.name == "snow":
            self.img = self.img_snow
        else:
            self.img = self.img_grass
        super().draw(*args, **kwargs)
