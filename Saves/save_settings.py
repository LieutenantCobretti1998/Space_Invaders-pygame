import json
from pygame_menu import widgets

default_settings = {
    "left": "a",
    "right": "d",
    "up": "w",
    "down": "s"
}


def save_resolution_to_json(width: int, height: int) -> None:
    with open("Saves/resolution_config.json", "w") as res:
        json.dump(
            {
                "width": width,
                "height": height
            },
            res)


def save_volume_to_json(volume: int) -> None:
    with open("Saves/volume_config.json", "w") as vol:
        json.dump(
            {
                "volume_level": volume
            },
            vol)


def save_highest_score(score: int) -> None:
    with open("Saves/highest_score.json", "w") as key:
        json.dump(
            {
                "score": score
            },
            key)


def save_keys_to_json(keys: dict) -> None:
    with open("Saves/keys_config.json", "w") as key:
        json.dump(
            {
                "key_bindings": keys
            },
            key)


def restore_default_keys() -> None:
    with open("Saves/keys_config.json", "w") as key:
        json.dump(
            {
                "key_bindings": default_settings
            },
            key)


def load_resolution_from_json() -> (int, int):
    default_width, default_height = 1280, 720  # Default values
    try:
        with open("Saves/resolution_config.json", "r") as res:
            data = json.load(res)
            width = data["width"]
            height = data["height"]
            return width, height
    except FileNotFoundError:
        print("resolution_config.json not found")
        return default_width, default_height


def load_score_from_json() -> int:
    try:
        with open("Saves/highest_score.json", "r") as scr:
            score = json.load(scr)
            return score["score"]
    except (FileNotFoundError, json.JSONDecodeError):
        print("Score config file not found or contains invalid data.")
        return 0

def load_volume_from_json() -> int:
    try:
        with open("Saves/volume_config.json", "r") as vol:
            data = json.load(vol)
            return data["volume_level"]
    except (FileNotFoundError, json.JSONDecodeError):
        print("Volume config file not found or contains invalid data.")
        return 50  # Default value


def load_keys_from_json() -> dict:
    try:
        with open("Saves/keys_config.json", "r") as key:
            data = json.load(key)
            keys = data.get("key_bindings", default_settings)
            return keys
    except (FileNotFoundError, json.JSONDecodeError):
        print("Keys config not found or contains invalid data.")
        return default_settings
