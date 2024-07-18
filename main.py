import json
import shutil
from os import path
from PIL import Image


def load(name: str):
    with open("maps.json", "r") as file:
        map_data = json.load(file)[name]
    for i, column in enumerate(map_data):
        for j, tile in enumerate(column):
            if tile == "" or path.exists(f"map_parts/tex1_512x512_{tile}_3.png"):
                continue
            shutil.move(f"unfiltered/tex1_512x512_{tile}_3.png", f"map_parts/tex1_512x512_{tile}_3.png")


def compile_map(name: str):
    with open("maps.json", "r") as file:
        map_data = json.load(file)[name]

    map_image = Image.new("RGB", size=(len(map_data[0]) * 512, len(map_data) * 512), color=(255, 0, 255))

    for i, column in enumerate(map_data):
        for j, tile in enumerate(column):
            if tile == "":
                continue
            map_image.paste(Image.open(f"map_parts/tex1_512x512_{tile}_3.png"), (j * 512, i * 512))

    map_image.show()


if __name__ == "__main__":
    a = "cave_of_phosphorescent_flowers"
    load(a)
    compile_map(a)
