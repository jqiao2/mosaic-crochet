import math
from enum import Enum

import cv2
import numpy as np
from PIL import Image

from src.utils import safe_get_grid

IMAGE_PATH = "../images/example/kraken.png"
WIDTH = 75


class Color(Enum):
    WHITE = 0
    BLACK = 1


class Stitch:
    def __init__(self, is_double: bool, color: Color = Color.WHITE, child=None, grandchild=None):
        """

        :param is_double:   double stitch or single stitch
        :param color:       WHITE or BLACK
        :param child:       stitch below this stitch; must be other color
        :param grandchild:  stitch two below this stitch; must be this color
        """
        if child:
            assert (child.COLOR != color)
        if grandchild:
            assert (grandchild.COLOR == color)

        self.is_double = is_double
        self.COLOR = color
        self.display_color = color

        self.child = child
        self.grandchild = grandchild

    def __repr__(self):
        ret = ""
        ret += str(self.COLOR) + " "
        ret += "double" if self.is_double else "single"
        return ret


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


def gen_grid(img: np.ndarray):
    assert (len(img.shape) == 2)  # greyscale image

    # first_color = Color.WHITE if np.average(img[-1]) > 128 else Color.BLACK

    height, width = img.shape

    stitch_grid = np.empty(img.shape, dtype=Stitch)

    # initialize grid that starts with a white row
    # TODO: make first row color configurable
    for h in reversed(range(height)):
        color = Color.WHITE if h % 2 == 0 else Color.BLACK
        for w in range(width):
            stitch_grid[h, w] = Stitch(False, color, safe_get_grid(stitch_grid, h + 1, w),
                                       safe_get_grid(stitch_grid, h + 2, w))

    save_stitch_grid(stitch_grid, "../images/example/kraken_only_single_stitches.png")

    # start from bottom, go up
    THRESH = 128
    for h in reversed(range(height)):
        for w in range(width):
            current_stitch = stitch_grid[h, w]
            current_stitch.display_color = Color.WHITE if img[h, w] > THRESH else Color.BLACK

            if current_stitch.display_color != current_stitch.COLOR:
                if current_stitch.child:
                    # if this stitch is not shown then the stitch below must be shown
                    current_stitch.child.display_color = current_stitch.child.COLOR
                else:
                    # No child so current stitch has to be the original color
                    current_stitch.display_color = current_stitch.COLOR
            elif current_stitch.child and current_stitch.child.display_color == current_stitch.COLOR:
                # we should cover the stitch below with a double crochet
                current_stitch.is_double = True

    return stitch_grid


def save_stitch_grid(stitch_grid: np.ndarray, filename="kraken_mosaic_grid.png"):
    assert (stitch_grid.dtype == Stitch)

    def get_stitch_color(stitch: Stitch):
        match stitch.display_color:
            case Color.BLACK:
                return 0
            case Color.WHITE:
                return 255
            case _:
                return 0

    v_get_stitch_color = np.vectorize(get_stitch_color)

    stitch_img = v_get_stitch_color(stitch_grid)

    Image.fromarray(stitch_img.astype(np.uint8)).save(filename)


if __name__ == '__main__':
    image = get_bw_image(IMAGE_PATH)
    Image.fromarray(image).save("result.png")

    small_img = get_stitch_size_image(image)
    Image.fromarray(small_img).save("small.png")

    # temp: read small image from disk
    # small_img = cv2.imread("small.png", cv2.IMREAD_GRAYSCALE)

    grid = gen_grid(small_img)
    save_stitch_grid(grid)
