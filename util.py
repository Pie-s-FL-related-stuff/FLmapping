import json
from PIL import Image


def get_map_data() -> dict[str, list[list[str]]]:
    with open("maps.json", "r") as file:
        map_data = json.load(file)
    return map_data


def get_tile(map_name: str, x: int, y: int, tile: str) -> Image.Image:
    if tile != "":
        return Image.open(f"map_parts/tex1_512x512_{tile}_3_mip0.png")
    try:
        return Image.open(f"missing_parts/{map_name}/{y + 1}_{x + 1}.png")
    except FileNotFoundError:
        print(f"Missing tile at {(x + 1, y + 1)} in {map_name} (might mess with automatic cropping)")
        return Image.new("RGB", size=(512, 512), color=(0, 255, 0))


def get_top_left_corner(image: Image.Image) -> tuple[int, int]:
    pixel_map = image.convert("RGB").load()
    for i in range(image.width * image.height):
        x, y = divmod(i, image.height)
        if pixel_map[x, y] != (255, 0, 255):
            return x, y
    return 0, 0


def get_down_right_corner(image: Image.Image) -> tuple[int, int]:
    pixel_map = image.load()
    for i in range(image.width * image.height - 1, 0, -1):
        x, y = divmod(i, image.height)
        if pixel_map[x, y] != (255, 0, 255):
            return x + 1, y + 1
    return image.width, image.height
