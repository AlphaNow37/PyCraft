from PIL import Image


def to_rgb(path, to_color: tuple[int, int, int], save_path):
    final_color = [val/256 for val in to_color]
    image: Image.Image = Image.open(path).convert("L")
    new_image = Image.new("RGBA", image.size)
    for y in range(image.height):
        for x in range(image.width):
            pixel = image.getpixel((x, y))
            vals = tuple(int(val*pixel) for val in final_color)+(255, )
            if vals == (0, 0, 0, 255):
                vals = (*to_color, 100)
            new_image.putpixel((x, y), vals)
    new_image.save(save_path)


if __name__ == '__main__':
    for name in ["spruce"]:
        path = f"src/leaves/{name}_leaves.png"
        save_path = f"../src/blocks/vegetation/leaves/{name}_leaves.png"
        to_rgb(path, (0, 100, 0), save_path)
