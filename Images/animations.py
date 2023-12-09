import pygame
import os


def background_image_animated(width: int, height: int, filename: str) -> list:
    frames = []
    for i in range(0, len(os.listdir(filename))):
        menu_frame = pygame.image.load(f"{filename}/frame{i}.png")
        scaled_frame = pygame.transform.scale(menu_frame, (width, height))
        frames.append(scaled_frame)
    return frames


def explosion_animation(size: tuple, filename: str, hit_type: str) -> list:
    if hit_type == "rocket":
        frames_rocket = [pygame.transform.scale(pygame.image.load(f"{filename}/Explosion_{num}.png"),
                                                size) for num in range(1, len(os.listdir(filename)))]
        return frames_rocket

    else:
        bullet_rockets = [pygame.transform.scale(pygame.image.load(f"{filename}/Explosion_{num}.png"),
                                                size) for num in range(1, len(os.listdir(filename)))]
        return bullet_rockets
