import pygame


class ShipCharacteristics:
    def __init__(self, surface: pygame.Surface, font_size: int, font_color: tuple):
        self.surface = surface
        self.font = pygame.font.SysFont("arial", font_size)
        self.font_color = font_color
        self.y_pos = 10

    def draw_health_amount(self, health) -> None:
        x_pos = 0
        match self.surface.get_width():
            case 1280:
                margin_health = 10
                x_pos += margin_health
            case 1366:
                margin_health = 30
                x_pos += margin_health
            case 1600:
                margin_health = 50
                x_pos += margin_health
        health_text = self.font.render(f"Health: {health}", True, self.font_color)
        self.surface.blit(health_text, (x_pos, self.y_pos))

    def draw_bullet_amount(self, bullets, reloading) -> None:
        x_pos = 0
        match self.surface.get_width():
            case 1280:
                margin_bullet = 420
                x_pos += margin_bullet
            case 1366:
                margin_bullet = 470
                x_pos += margin_bullet
            case 1600:
                margin_bullet = 520
                x_pos += margin_bullet
        bullets_amount = self.font.render(f"Bullets: {bullets}", True, self.font_color)
        if reloading:
            bullets_amount = self.font.render(f"Reloading", True, self.font_color)
        self.surface.blit(bullets_amount, (x_pos, self.y_pos))

    def draw_rocket_amount(self, rockets, reloading) -> None:
        x_pos = 0
        match self.surface.get_width():
            case 1280:
                margin_rocket = 760
                x_pos = 0 + margin_rocket
            case 1366:
                margin_rocket = 830
                x_pos += margin_rocket
            case 1600:
                margin_rocket = 900
                x_pos += margin_rocket
        rockets_amount = self.font.render(f"Rockets: {rockets}", True, self.font_color)
        if reloading:
            rockets_amount = self.font.render(f"Reloading", True, self.font_color)
        self.surface.blit(rockets_amount, (x_pos, self.y_pos))

