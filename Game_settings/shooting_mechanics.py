import pygame
from pygame.sprite import Sprite, Group
import random


class Bullet(Sprite):
    def __init__(self, surface, ship_x, ship_y, position):
        Sprite.__init__(self)
        self.surface = surface
        self.position_x = ship_x
        self.position_y = ship_y - 50
        self.speed = 4
        self.image = pygame.image.load("Images/bullets_sprite/spr_bullet_strip03.png").convert_alpha(self.surface)
        self.rect = self.image.get_rect()

        match position:
            case "left":
                self.rect.left = self.position_x - 35

            case "right":
                self.rect.right = self.position_x + 35

    def update(self):
        self.position_y -= self.speed
        self.rect.y = self.position_y


class Rocket(Sprite):
    def __init__(self, surface, ship_x, ship_y):
        Sprite.__init__(self)
        self.surface = surface
        self.position_x = ship_x
        self.position_y = ship_y - 150
        self.speed = 4
        self.image = pygame.image.load("Images/bullets_sprite/laserBulletcopy.png").convert_alpha(self.surface)
        self.rect = self.image.get_rect()
        self.rect.centerx = self.position_x
        self.rect.top = self.position_y

    def update(self) -> None:
        self.position_y -= self.speed
        self.rect.y = self.position_y


class EnemyProjectTile(Sprite):
    def __init__(self, surface: pygame.Surface, x, y, x_velocity):
        super().__init__()
        self.surface = surface
        self.image = pygame.image.load("Images/bullets_sprite/spr_bullet_strip03.png").convert_alpha(self.surface)
        self.rect = self.image.get_rect(center=(x, y))
        self.x_velocity = x_velocity

    def update(self) -> None:
        self.rect.y += 5
        self.rect.x += self.x_velocity

    def fire(self, bullet_group: Group, bullet) -> None:
        bullet.update()
        # print(bullet.rect.bottom)
        if self.rect.bottom < 0 or self.rect.top > self.surface.get_height():
            bullet_group.remove(bullet)
            bullet.kill()

