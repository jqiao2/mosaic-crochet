import numpy as np
from matplotlib import pyplot as plt


def show_image(img: np.ndarray, greyscale=False):
    plt.imshow(img, cmap="gray" if greyscale else "viridis", interpolation='nearest')
    # plt.show()


def safe_get_grid(grid, h, w):
    try:
        return grid[h, w]
    except IndexError:
        return None
