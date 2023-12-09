import pygame
import time
from pygame.sprite import Group, Sprite
from Game_settings import shooting_mechanics


class Ship(Sprite):
    def __init__(self, surface: pygame.Surface):
        super().__init__()
        self.surface = surface
        self.position_x = float(self.surface.get_width() // 2)
        self.position_y = float(self.surface.get_height())
        self.speed = 5
        self.boost = 3.5
        self.max_health = 100
        self.current_health = self.max_health
        self.health_bar_length = 50
        self.health_bar_width = 5
        self.health_bar_color = (0, 255, 0)
        self.bullet_class = shooting_mechanics.Bullet
        self.rocket_class = shooting_mechanics.Rocket
        self.bullets = Group()
        self.bullets_amount = 20
        self.rocket = Group()
        self.rockets_amount = 5
        self.ship_image = pygame.image.load("Images/space_ships/fighter.png")
        self.rect = self.ship_image.get_rect()
        self.bullets_reloading_time = 0
        self.bullets_reloading = False
        self.rockets_reloading_time = 0
        self.rockets_reloading = False
        self.ship_position()

    def start_bullets_reloading(self):
        self.bullets_reloading = True
        self.bullets_reloading_time = time.time()

    def check_bullet_reloading(self):
        if self.bullets_reloading and (time.time() - self.bullets_reloading_time > 5):
            self.bullets_reloading = False
            self.bullets_amount = 20

    def start_rockets_reloading(self):
        self.rockets_reloading = True
        self.rockets_reloading_time = time.time()

    def check_rockets_reloading(self):
        if self.bullets_reloading and (time.time() - self.rockets_reloading_time > 5):
            self.rockets_reloading = False
            self.rockets_amount = 5

    def ship_position(self) -> None:
        self.rect.centerx = int(self.position_x)
        self.rect.bottom = int(self.position_y)

    def create_ship(self) -> None:
        self.surface.blit(self.ship_image, self.rect)

    def draw_health_bar(self) -> None:
        current_length = (self.current_health / self.max_health) * self.health_bar_length

        health_bar_x = self.rect.centerx - self.health_bar_length // 2
        health_bar_y = self.rect.bottom + 10
        if 20 <= self.current_health <= 50:
            self.health_bar_color = (240, 245, 29)
        elif self.current_health < 20:
            self.health_bar_color = (255, 0, 0)

        pygame.draw.rect(self.surface, (0, 0, 255),
                         (health_bar_x, health_bar_y, self.health_bar_length, self.health_bar_width))

        pygame.draw.rect(self.surface, self.health_bar_color,
                         (health_bar_x, health_bar_y, current_length, self.health_bar_width))

    def decrease_health_bar(self, amount):
        self.current_health = max(self.current_health - amount, 0)

    def display_gameover_menu(self, display: pygame.Surface, font_size, font_color):
        font = pygame.font.SysFont("arial", font_size)
        game_over_text = font.render("Game Over", True, font_color)
        restart_text = font.render("Press 'R' to restart", True, font_color)
        exit_text = font.render("Press 'Space' to return Main Menu", True, font_color)

        text_rect = game_over_text.get_rect(center=(display.get_width() // 2, display.get_height() // 2 - 50))
        restart_rect = restart_text.get_rect(center=(display.get_width() // 2, display.get_height() // 2))
        exit_rect = exit_text.get_rect(center=(display.get_width() // 2, display.get_height() // 2 + 50))
        display.blit(game_over_text, text_rect)
        display.blit(restart_text, restart_rect)
        display.blit(exit_text, exit_rect)

    def update_movements(self, left, right, up, down) -> None:
        keys = pygame.key.get_pressed()

        # Ship boost
        current_speed = self.speed * (self.boost if keys[pygame.K_LSHIFT] or keys[pygame.K_RSHIFT] else 1)
        # print(current_speed)

        # Left movement
        match (keys[pygame.key.key_code(left)], self.rect.left > 0):
            case (True, True):
                self.position_x -= current_speed

        # Right movement
        match (keys[pygame.key.key_code(right)], self.rect.right < self.surface.get_width()):
            case (True, True):
                self.position_x += current_speed

        # Vertical movement
        match (keys[pygame.key.key_code(up)], self.rect.top > 0):
            case (True, True):
                self.position_y -= current_speed

        # Go back
        match (keys[pygame.key.key_code(down)], self.rect.bottom < self.surface.get_height()):
            case (True, True):
                self.position_y += current_speed

        # Update the ship rect after changing position
        self.ship_position()

    def shooting(self, ship_side):
        match ship_side:
            case "left":
                if not self.bullets_reloading:
                    left_bullet = self.bullet_class(self.surface, self.position_x, self.position_y, "left")
                    self.bullets.add(left_bullet)
                    self.bullets_amount = max(self.bullets_amount - 1, 0)
                    if self.bullets_amount == 0:
                        self.start_bullets_reloading()
                else:
                    self.check_bullet_reloading()
            case "right":
                if not self.bullets_reloading:
                    right_bullet = self.bullet_class(self.surface, self.position_x, self.position_y, "right")
                    self.bullets.add(right_bullet)
                    self.bullets_amount = max(self.bullets_amount - 1, 0)
                    if self.bullets_amount == 0:
                        self.start_bullets_reloading()
                else:
                    self.check_bullet_reloading()

    def rocket_launch(self):
        if not self.rockets_reloading:
            rocket = self.rocket_class(self.surface, self.position_x, self.position_y)
            self.rocket.add(rocket)
            self.rockets_amount = max(self.rockets_amount - 1, 0)
            if self.rockets_amount == 0:
                self.start_rockets_reloading()
        else:
            self.check_rockets_reloading()

    def update_bullets(self):
        self.bullets.update()
        for bullet in self.bullets.copy():
            if bullet.rect.bottom < 0:
                self.bullets.remove(bullet)

            self.bullets.draw(self.surface)

    def update_rockets(self):
        self.rocket.update()
        for rocket in self.rocket.copy():
            if rocket.rect.bottom < 0:
                self.rocket.remove(rocket)
            self.rocket.draw(self.surface)
