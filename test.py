# import pygame
# print(pygame.font.get_fonts())
import pygame
import sys

pygame.init()
screen = pygame.display.set_mode((800, 600))
clock = pygame.time.Clock()

class MenuItem:
    def __init__(self, text, action):
        self.text = text
        self.action = action
        self.is_selected = False

    def draw(self, surface, x, y):
        font = pygame.font.SysFont(None, 36)
        color = (255, 0, 0) if self.is_selected else (255, 255, 255)
        text_surf = font.render(self.text, True, color)
        surface.blit(text_surf, (x, y))

def start_game():
    print("Game Started")

def settings_menu():
    print("Settings Menu")

def quit_game():
    pygame.quit()
    sys.exit()

menu_items = [
    MenuItem("Start Game", start_game),
    MenuItem("Settings", settings_menu),
    MenuItem("Quit", quit_game),
]

selected_index = 0
while True:
    screen.fill((0, 0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_DOWN:
                selected_index = (selected_index + 1) % len(menu_items)
            if event.key == pygame.K_UP:
                selected_index = (selected_index - 1) % len(menu_items)
            if event.key == pygame.K_RETURN:
                menu_items[selected_index].action()

    for i, item in enumerate(menu_items):
        item.is_selected = i == selected_index
        item.draw(screen, 350, 200 + i * 50)

    pygame.display.flip()
    clock.tick(60)

