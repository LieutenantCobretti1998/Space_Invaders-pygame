import pygame_menu


main_font = pygame_menu.font.FONT_DIGITAL
pause_font = pygame_menu.font.FONT_FIRACODE_BOLD_ITALIC

menu_transpareny_theme = pygame_menu.Theme(background_color=(0, 0, 0, 2),
                                           title_background_color=(75, 123, 186, 204),
                                           title_font_color=(180, 0, 129, 2),
                                           widget_font_color=(81, 12, 177, 2),
                                           widget_padding=5,
                                           widget_font=main_font)


menu_black_background = pygame_menu.Theme(background_color=(0, 0, 0, 70),
                                          title_background_color=(75, 123, 186, 204),
                                          title_font_color=(180, 0, 129, 2),
                                          widget_font_color=(150, 162, 86, 1),
                                          widget_padding=5,
                                          widget_font=pause_font
                                          )
