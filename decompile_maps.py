"""
Turns full maps back into map tiles that work for Citra texture packs.
"""
from PIL import Image
from util import get_map_data, get_tile, get_top_left_corner
from os import mkdir


def add_pink_borders(map_name: str, upscale_factor: float) -> Image.Image:
    map_data = get_map_data()[map_name]

    size = (int(512 * len(map_data[0]) * upscale_factor), int(512 * len(map_data) * upscale_factor))
    image = Image.new("RGB", size=size, color=(255, 0, 255))

    top_left_corner = get_top_left_corner(get_tile(map_name, 0, 0, map_data[0][0]))

    image.paste(Image.open(f"edited_maps/{map_name}.png"), (int(top_left_corner[0] * upscale_factor), int(top_left_corner[1] * upscale_factor)))

    return image


def decompile_map(map_name: str, upscale_factor: float):
    map_data = get_map_data()[map_name]

    edited_map = Image.open(f"edited_maps/{map_name}.png")

    try:
        mkdir(f"edited_tiles/{map_name}")
    except FileExistsError:
        pass

    for i in range(len(map_data)):
        for j in range(len(map_data[0])):
            tile_name = map_data[i][j]
            if tile_name == "":
                continue
            edited_tile = edited_map.crop((j * 512 * upscale_factor, i * 512 * upscale_factor, (j + 1) * 512 * upscale_factor, (i + 1) * 512 * upscale_factor))
            edited_tile.save(f"edited_tiles/{map_name}/tex1_512x512_{tile_name}_3.png")
