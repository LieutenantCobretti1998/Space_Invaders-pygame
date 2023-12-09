import os
import random
import re
import pygame
from pygame import Surface


def get_image_files(directory: str) -> list:
    supported_formats = ["png", "jpeg", "jpg"]
    pattern = re.compile(r"1\.png$", re.I)
    image_files: list[str] = [os.path.join(directory, file) for file in os.listdir(directory)
                              if os.path.isfile(os.path.join(directory, file))
                              and any(file.lower().endswith(f'.{ext}') for ext in supported_formats)
                              and pattern.search(file)]
    return image_files


def load_random_enemy(enemy_images: list) -> Surface:
    random_image = random.choice(enemy_images)
    image = pygame.transform.scale(pygame.image.load(random_image), (95, 95))
    return image
