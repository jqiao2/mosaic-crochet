from pathlib import Path

from PIL import Image

from src.algo import generate_closest_grid, get_bw_image, get_stitch_size_image
from src.constants import IMAGE_PATH
from src.objects import Stitch
from src.utils import save_stitch_grid


def generate_stitch_grid(filepath: str):
    path = Path(filepath)

    bw_image = get_bw_image(filepath)
    Image.fromarray(bw_image).save("../output/{}_bw.png".format(path.stem))

    small_image = get_stitch_size_image(bw_image)
    Image.fromarray(small_image).save("../output/{}_small.png".format(path.stem))

    # grid = generate_closest_grid(small_image, 250, False)
    grid = generate_closest_grid(small_image)
    save_stitch_grid(grid, "../output/{}_mosaic_grid.png".format(path.stem))


if __name__ == '__main__':
    s = Stitch(True, True)
    # generate_stitch_square(s)
    generate_stitch_grid(IMAGE_PATH)
