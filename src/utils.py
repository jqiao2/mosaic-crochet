import numpy as np
from PIL import Image, ImageDraw
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


def create_image(size=20, line_color=(0, 0, 0), grid_color=(200, 200, 200), bg_color=(255, 255, 255), line_width=1,
                 draw_x=False):
    """
    Generate a square PNG image with optional X hiding grid lines.
    """
    # Create a new image with background color
    image = Image.new('RGB', (size, size), bg_color)

    # Create a drawing context
    draw = ImageDraw.Draw(image)

    # Draw grid lines only if no X is present
    if draw_x:
        draw.line([(0, size - 1), (0, 0), (size - 1, 0), (size - 1, size - 1)],
                  fill=grid_color, width=1)
    else:
        draw.line([(size - 1, 0), (size - 1, size - 1), (0, size - 1), (0, 0)],
                  fill=grid_color, width=1)

    # Draw X if specified
    if draw_x:
        # Calculate the coordinates for the smaller X
        x_size = size // 2  # X will be half the image size
        start_x = (size - x_size) // 2
        start_y = (size - x_size) // 2

        # Draw the first diagonal line (top-left to bottom-right)
        draw.line([
            (start_x, start_y),
            (start_x + x_size - 1, start_y + x_size - 1)
        ], fill=line_color, width=line_width)

        # Draw the second diagonal line (top-right to bottom-left)
        draw.line([
            (start_x + x_size - 1, start_y),
            (start_x, start_y + x_size - 1)
        ], fill=line_color, width=line_width)

    return image


def save_image_grid(x_pattern, image_size=20, grid_color=(200, 200, 200), false_color=(0, 0, 0),
                    true_color=(255, 255, 255)):
    """
    Create a grid of images with X pattern and hidden grid lines.
    """
    h, w = len(x_pattern), len(x_pattern[0])

    # Create a new image for the entire grid
    grid_image = Image.new('RGB', (image_size * w, image_size * h), true_color)

    # Generate and place individual images
    for row in range(h):
        for col in range(w):
            # Create individual image
            x_color = false_color if x_pattern[row][col].display_color else true_color
            bg_color = true_color if x_pattern[row][col].display_color else false_color
            single_image = create_image(
                size=image_size,
                line_color=x_color,
                grid_color=grid_color,
                bg_color=bg_color,
                draw_x=x_pattern[row][col].is_double
            )

            # Calculate position to paste the image
            paste_x = col * image_size
            paste_y = row * image_size

            # Paste the image into the grid
            grid_image.paste(single_image, (paste_x, paste_y))

    return grid_image


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
    stitch_img = save_image_grid(x_pattern=stitch_grid)
    stitch_img.save(filename)
