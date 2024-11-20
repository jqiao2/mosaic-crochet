import numpy as np
from PIL import Image
from matplotlib import pyplot as plt

from src.objects import Stitch


def show_image(img: np.ndarray, greyscale=False):
    plt.imshow(img, cmap="gray" if greyscale else "viridis", interpolation='nearest')
    # plt.show()


def safe_get_grid(grid, h, w):
    try:
        return grid[h, w]
    except IndexError:
        return None


def get_stitch_color(stitch: Stitch):
    """
    True: white
    False: black
    """
    if stitch.display_color:
        return 255.0
    else:
        return 0


def gen_stitch_grid_img(stitch_grid: np.ndarray):
    assert (stitch_grid.dtype == Stitch)
    v_get_stitch_color = np.vectorize(get_stitch_color)
    return v_get_stitch_color(stitch_grid)


def save_stitch_grid(stitch_grid: np.ndarray, filename: str):
    assert (stitch_grid.dtype == Stitch)
    stitch_img = gen_stitch_grid_img(stitch_grid)
    Image.fromarray(stitch_img.astype(np.uint8)).save(filename)
