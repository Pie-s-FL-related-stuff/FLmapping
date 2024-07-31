from typing import Callable
from util import get_map_data


def ask(question: str, valid: Callable[[str], bool], error_message: str) -> str:
    while True:
        response = input(f"{question}\n\t")
        if valid(response):
            return response
        print(error_message)


def main():
    task = ask("- [1] Tiles to map\n- [2] Map to tiles", lambda x: x in ("1", "2"), "Invalid option")
    match task:
        case "1":
            from compile_maps import compile_map
            map_name = ask("Enter the map name", lambda x: x in get_map_data().keys(), "Invalid map name (use the names as found in maps.json)")
            map_image = compile_map(map_name)
            if ask("Do you want to remove the pink borders? (Y/N)", lambda x: x.upper() in ("Y", "N"), "Invalid option").upper() == "Y":
                from compile_maps import remove_borders
                map_image = remove_borders(map_image)
            map_image.save(f"full_maps/{map_name}.png")
        case "2":
            from decompile_maps import decompile_map
            map_name = ask("Enter the map name", lambda x: x in get_map_data().keys(), "Invalid map name (use the names as found in maps.json)")
            upscale_factor = float(ask("Enter the upscale factor", lambda x: x.replace(".", "", 1).isdigit(), "Invalid upscale factor"))
            if ask("Does the map already have pink borders? (Y/N)", lambda x: x.upper() in ("Y", "N"), "Invalid option").upper() == "N":
                from decompile_maps import add_pink_borders
                add_pink_borders(map_name, upscale_factor).save(f"edited_maps/{map_name}.png")
            decompile_map(map_name, upscale_factor)
    print("Done!")


if __name__ == "__main__":
    main()
