import json
from PIL import Image


MAP = "deep_elderwood"


def get_tile(map_name: str, x: int, y: int, tile: str) -> Image.Image:
    if tile != "":
        return Image.open(f"map_parts/tex1_512x512_{tile}_3_mip0.png")
    try:
        return Image.open(f"missing_parts/{map_name}/{y + 1}_{x + 1}.png")
    except FileNotFoundError:
        print(f"Missing tile at {(x + 1, y + 1)} in {map_name} (might mess with automatic cropping)")
        return Image.new("RGB", size=(512, 512), color=(0, 255, 0))


def compile_map(map_name: str):
    with open("maps.json", "r") as file:
        map_data = json.load(file)[map_name]

    map_image = Image.new("RGB", size=(len(map_data[0]) * 512, len(map_data) * 512), color=(0, 255, 0))

    for i, column in enumerate(map_data):
        for j, tile in enumerate(column):
            map_image.paste(get_tile(map_name, j, i, tile), (j * 512, i * 512))

    return map_image


def remove_borders(image: Image.Image) -> Image.Image:
    pixel_map = image.load()

    top_left = (0, 0)
    down_right = (512, 512)

    for i in range(0, image.width * image.height):
        x, y = divmod(i, image.height)
        if pixel_map[x, y] != (255, 0, 255):
            top_left = (x, y)
            break

    for i in range(image.width * image.height - 1, 0, -1):
        x, y = divmod(i, image.height)
        if pixel_map[x, y] != (255, 0, 255):
            down_right = (x + 1, y + 1)
            break

    return image.crop((top_left[0], top_left[1], down_right[0], down_right[1]))


if __name__ == "__main__":
    with open("maps.json", "r") as file:
        maps = json.load(file)

    for map_name in maps:
        map_image = compile_map(map_name)
        map_image = remove_borders(map_image)
        map_image.save(f"full_maps/{map_name}.png")
