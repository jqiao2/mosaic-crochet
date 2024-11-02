import statistics
from enum import Enum
from pprint import pprint

import imageio.v2 as imageio
import cv2
import numpy as np
from PIL import Image

IMAGE_PATH = "../images/20645ef1fef97cb5c45e9521c4153507-4283932324.jpg"
WIDTH = 75


class Color(Enum):
    WHITE = 0
    BLACK = 1


class Stitch:
    def __init__(self, is_double, color=Color.WHITE):
        self.is_double = is_double
        self.color = color


def get_bw_image(image_path: str, threshold: int = 60):
    im_gray = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    (thresh, im_bw) = cv2.threshold(im_gray, 128, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
    return im_bw


def convert_to_grid(img, width_stitches=WIDTH):
    assert (len(img.shape) == 2)  # greyscale image

    h, w = img.shape
    print(img.shape)

    height_stitches = round(h / w * width_stitches)
    print("Generate crochet pattern {} by {}".format(width_stitches, height_stitches))

    # split horizontally

    return None


if __name__ == '__main__':
    image = get_bw_image(IMAGE_PATH)
    Image.fromarray(image).save("result.png")

    convert_to_grid(image)
