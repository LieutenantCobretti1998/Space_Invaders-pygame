import random
import pygame
from pygame.sprite import Group, Sprite
from Images import enemy_randomization
from Game_settings import shooting_mechanics
image_files = enemy_randomization.get_image_files("Images/aliens/Spaceships-3")

spread_values = [-2, 0, 2]


class Aliens(Sprite):
    def __init__(self, surface, previous_x_position):
        super().__init__()
        self.surface = surface
        self.image = enemy_randomization.load_random_enemy(image_files)
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, self.surface.get_width() - self.rect.width)
        adjustment_factor = self.surface.get_width() * 0.05  # 5% of screen width
        if abs(self.rect.x - previous_x_position) <= 10:
            self.rect.x += adjustment_factor
            self.rect.x = min(self.rect.x, self.surface.get_width() - self.rect.width)

        self.rect.y = -self.rect.height

    def update(self) -> None:
        self.rect.y += 2

    @staticmethod
    def update_enemies(aliens: Group, surface: pygame.display) -> None:
        aliens.update()
        for alien in aliens.copy():
            if alien.rect.top > surface.get_height():
                aliens.remove(alien)
            aliens.draw(surface)

    def fire_launch(self) -> Sprite:
        projectile = shooting_mechanics.EnemyProjectTile(self.surface, self.rect.centerx, self.rect.bottom,
                                                         random.choice(spread_values))
        return projectile


