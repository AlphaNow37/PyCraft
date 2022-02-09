from PIL import Image
import pathlib
import numpy

src_path = pathlib.Path(__file__).parent / "src"
img = Image.open(src_path / "from" / "clouds.png").convert("RGBA")
array = numpy.array(img)
new_array = numpy.zeros((153, 153, 4), numpy.uint8)

blue_array = [90, 194, 233, 255]
white_array = [0, 0, 0, 0]
black_array = [0, 0, 0, 255]

width = array.shape[1]
for y, line in enumerate(array[1::4]):
    for x, pixel in enumerate(line[::4]):
        pixel: numpy.ndarray
        if numpy.array_equal(pixel, blue_array) or numpy.array_equal(pixel, black_array):
            new_array[y][x] = white_array
        else:
            new_array[y][x] = pixel

height_line = 152//4
width_row = 152//2

arrays = [new_array[height_line*y+2:height_line*y+height_line+2, width_row*x:width_row*x+width_row]
          for x in range(2) for y in range(4)]
imgs = [Image.fromarray(array, "RGBA") for array in arrays]
for i, img in enumerate(imgs):
    img.save(src_path / "final" / f"clouds_{i}.png")
