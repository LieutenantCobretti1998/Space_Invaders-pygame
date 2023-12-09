import pygame
from Saves import save_settings


class ScoreBoard:
    def __init__(self, surface: pygame.Surface, font_size: int, font_color: tuple):
        self.score = 0
        self.margin = 170
        self.surface = surface
        self.font = pygame.font.SysFont("arial", font_size)
        self.font_color = font_color
        self.x_pos = self.surface.get_width() - self.margin
        self.y_pos = 10

    def draw(self, display) -> None:
        score_text = self.font.render(f"Score: {self.score}", True, self.font_color)
        display.blit(score_text, (self.x_pos, self.y_pos))

    def update(self, value) -> None:
        self.score += value


class HighestScore(ScoreBoard):
    def __init__(self, surface: pygame.Surface, font_size: int, font_color: tuple, *args):
        super().__init__(surface, font_size, font_color)
        try:
            self.highest_score = args[0]
        except FileNotFoundError:
            self.highest_score = 0

        self.x_pos = self.surface.get_width() - self.margin - 20
        self.y_pos = 50

    def draw(self, display) -> None:
        score_text = self.font.render(f"Highest Score: {self.highest_score}", True, self.font_color)
        display.blit(score_text, (self.x_pos, self.y_pos))

    def update(self, **kwargs) -> None:
        self.highest_score = kwargs['highest_score']
