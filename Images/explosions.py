import pygame
from pygame.sprite import Group, Sprite
from Images import animations

bullets_explosion = animations.explosion_animation((95, 95), "Images/PNG/Explosion_3", "bullets")
rockets_explosion = animations.explosion_animation((120, 120), "Images/PNG/Explosion_6", "rockets")
rocket_bigBoom = animations.explosion_animation((250, 250), "Images/PNG/Explosion_6", "rockets")


class Explosion(Sprite):
    def __init__(self, surface, center, explosion_type):
        super().__init__()
        self.surface = surface
        self.current_frame = 0
        self.frame_rate = 10
        self.last_update = pygame.time.get_ticks()
        self.explosion_type = explosion_type

        # Choose frames based on explosion type
        if self.explosion_type == "rocket":
            self.frames = rockets_explosion

        elif self.explosion_type == "big_boom":
            self.frames = rocket_bigBoom

        else:
            self.frames = bullets_explosion

        self.image = self.frames[self.current_frame]
        self.rect = self.image.get_rect(center=center)

    def update(self) -> None:
        now = pygame.time.get_ticks()
        if now - self.last_update > self.frame_rate:
            self.last_update = now
            self.current_frame += 1
            if self.current_frame == len(self.frames):
                self.kill()  # Remove explosion after last frame
            else:
                center = self.rect.center
                self.image = self.frames[self.current_frame]
                self.rect = self.image.get_rect(center=center)




