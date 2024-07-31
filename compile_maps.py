"""
Turns map tiles (as found in the game) into full maps.
"""
from PIL import Image
from util import get_map_data, get_top_left_corner, get_down_right_corner, get_tile

MAP = "deep_elderwood"


def compile_map(map_name: str):
    map_data = get_map_data()[map_name]

    map_image = Image.new("RGB", size=(len(map_data[0]) * 512, len(map_data) * 512), color=(0, 255, 0))

    for i, column in enumerate(map_data):
        for j, tile in enumerate(column):
            map_image.paste(get_tile(map_name, j, i, tile), (j * 512, i * 512))

    return map_image


def remove_borders(image: Image.Image) -> Image.Image:
    return image.crop((*get_top_left_corner(image), *get_down_right_corner(image)))

