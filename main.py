import json
from PIL import Image


MAP = "west_grassy_plains"


class MissingTileError(Exception):
    def __init__(self, map_name: str, x: int, y: int):
        super().__init__(f"Missing tile at {(x + 1, y + 1)} in {map_name}")


def get_tile(map_name: str, x: int, y: int, tile: str) -> Image.Image:
    if tile != "":
        return Image.open(f"map_parts/tex1_512x512_{tile}_3.png")
    try:
        return Image.open(f"missing_parts/{map_name}/{y + 1}_{x + 1}.png")
    except FileNotFoundError:
        raise MissingTileError(map_name, x, y)


def compile_map(map_name: str):
    with open("maps.json", "r") as file:
        map_data = json.load(file)[map_name]

    map_image = Image.new("RGB", size=(len(map_data[0]) * 512, len(map_data) * 512), color=(0, 255, 0))

    for i, column in enumerate(map_data):
        for j, tile in enumerate(column):
            map_image.paste(get_tile(map_name, j, i, tile), (j * 512, i * 512))

    map_image.show()


if __name__ == "__main__":
    compile_map(MAP)
