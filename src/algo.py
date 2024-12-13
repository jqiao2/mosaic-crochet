import math

import cv2
import numpy as np
from matplotlib import pyplot as plt

from src.constants import WIDTH
from src.objects import Stitch
from src.utils import get_stitch_color, gen_stitch_grid_img, save_stitch_grid, safe_get_grid


def get_bw_image(image_path: str):
    im_gray = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    (thresh, im_bw) = cv2.threshold(im_gray, 128, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
    return im_bw


def get_stitch_size_image(img: np.ndarray, width_stitches: int = WIDTH):
    assert (len(img.shape) == 2)  # greyscale image
    assert (len(np.unique(img)) <= 2)  # binary black/white image

    h, w = img.shape

    height_stitches = math.ceil(h / w * width_stitches)

    print("Generate crochet pattern {} by {}".format(width_stitches, height_stitches))

    img = cv2.resize(img, dsize=(width_stitches, height_stitches), interpolation=cv2.INTER_CUBIC)

    return img


def gen_grid(img: np.ndarray, first_stitch: bool = True, threshold=128):
    assert (len(img.shape) == 2)  # greyscale image

    # first_color = np.average(img[-1]) > 128

    height, width = img.shape

    stitch_grid = np.empty(img.shape, dtype=Stitch)

    # initialize grid that starts with a white row
    for h in reversed(range(height)):
        color = h % 2 == (0 if first_stitch else 1)
        for w in range(width):
            stitch_grid[h, w] = Stitch(False, color, safe_get_grid(stitch_grid, h + 1, w),
                                       safe_get_grid(stitch_grid, h + 2, w))

    # start from bottom, go up
    for h in reversed(range(height)):
        for w in range(width):
            current_stitch = stitch_grid[h, w]
            assert (isinstance(current_stitch, Stitch))  # suppress pycharm warnings

            current_stitch.display_color = img[h, w] > threshold

            if current_stitch.display_color != current_stitch.COLOR:
                if current_stitch.child:
                    # if this stitch is not shown then the stitch below must be shown
                    current_stitch.child.display_color = current_stitch.child.COLOR
                else:
                    # No child so current stitch has to be the original color
                    None
                    # current_stitch.display_color = current_stitch.COLOR
            elif current_stitch.child and current_stitch.child.display_color == current_stitch.COLOR:
                # we should cover the stitch below with a double crochet
                current_stitch.is_double = True

    return stitch_grid


def generate_closest_grid(img: np.ndarray, threshold: int = None, first_stitch: bool = None):
    if threshold:
        thresholds = {threshold}
    else:
        thresholds = {64, 96, 128, 160, 192, 224}
    if first_stitch:
        first_stitches = {first_stitch}
    else:
        first_stitches = {False, True}

    best_mean_sq = 2 ** 1000
    best_grid = None
    best_threshold = None
    best_first_stitch = None
    for first_stitch in first_stitches:
        for threshold in thresholds:
            grid = gen_grid(img, first_stitch, threshold)
            grid_img = gen_stitch_grid_img(grid)
            mean_sq = np.square(np.subtract(img, grid_img)).mean()
            print("first stitch: {}, threshold: {}, mean square: {}".format(first_stitch, threshold, mean_sq))
            if mean_sq < best_mean_sq:
                best_mean_sq = mean_sq
                best_grid = grid
                best_threshold = threshold
                best_first_stitch = first_stitch

    print(
        "best first stitch: {}, threshold: {}, mean square: {}".format(best_first_stitch, best_threshold, best_mean_sq))
    return best_grid


def generate_stitch_square(stitch: Stitch):
    square = np.zeros((20, 20))
    square[:] = get_stitch_color(stitch)

    if stitch.is_double:
        # draw x if double stitch
        x = [5, 15]
        y = [5, 15]
        print(x[::-1])
        plt.plot(x, y, color='black', linewidth=3)
        plt.plot(x[::-1], y, color='black', linewidth=3)

    plt.imshow(square, cmap="gray", vmin=0, vmax=255)
    plt.show()

    return None
