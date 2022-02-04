import pygame
from .. import Game


class PygameText:
    def __init__(self, game: Game, x=0, y=0, font: pygame.font.Font = None, text="...",
                 color_fond="black", alpha=70, color_text=(255, 255, 255), height=50, aligned="left", pad=5):
        self.height = height + pad*2
        if font is None:
            font = pygame.font.Font(None, 60)
        self.text: str = text
        lines = text.split("\n")
        lines_surfaces = [font.render(line, True, color_text) for line in lines]
        max_width = max(lines_surfaces, key=pygame.Surface.get_width).get_width()
        height = font.get_height()
        fond = pygame.Surface((max_width+pad*2, height*len(lines)+pad*2))
        fond.fill(color_fond)
        for y_, line in enumerate(lines_surfaces):
            width = line.get_width()
            if aligned == "left":
                fond.blit(line, (pad, y_*height+pad))
            elif aligned == "center":
                fond.blit(line, (max_width/2-width/2+pad, y_*height+pad))
            elif aligned == "right":
                fond.blit(line, (max_width-width-pad, y_*height+pad))
        fond.set_alpha(alpha)
        self.image = fond

        self.width = fond.get_width()*self.height/fond.get_height()

        self.game, self.x, self.y = game, x, y

    def draw(self):
        height = self.game.size_screen[1] * self.height/480
        width = self.width/self.height*height

        x = self.x * self.game.size_screen[1]/480
        y = self.y/self.height * height

        self.draw_with_size(x, y, width, height)

    def draw_xy_exact(self, x, y):
        height = self.game.size_screen[1] * self.height / 480

        width = self.width / self.height * height

        self.draw_with_size(x, y, width, height)

    def draw_with_size(self, x, y, width, height):
        new_img = pygame.transform.scale(self.image, (int(width), int(height)))

        self.game.screen.blit(new_img, (x, y))
