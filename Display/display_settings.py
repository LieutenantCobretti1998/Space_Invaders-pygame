import random
import pygame
from dataclasses import dataclass, field
from Images import animations

@dataclass
class Screen:
    width: int = field(default=1280)
    height: int = field(default=720)
    index: int = field(default=0)
    speed: int = field(default=3)

    def __post_init__(self):
        pygame.init()

        self.screen = pygame.display.set_mode((self.width, self.height))
        self.icon = pygame.image.load("Images/Space-Invaders-icon.png")
        pygame.display.set_icon(self.icon)

        pygame.display.set_caption("Space Invaders")
        backgrounds = ["Images/Menu_gif_frames", "Images/Inifinitepath_gif_frames", "Images/planetgif_frames"]
        self.random_back = random.choice(backgrounds)
        self.frames = animations.background_image_animated(self.width, self.height, self.random_back)
        self.clock = pygame.time.Clock()
        self.resolution_changed = False

    def change_resolution(self, value: str, resolution: str, callback=None) -> None:
        if callback is not None:
            callback()
        width, height = map(int, resolution.split("x"))
        self.width = width
        self.height = height
        pygame.display.set_mode((self.width, self.height))
        self.frames = animations.background_image_animated(self.width, self.height, self.random_back)
        self.resolution_changed = True

    @property
    def get_frames(self) -> list:
        return self.frames
