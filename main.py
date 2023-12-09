import pygame.event
from Display import display_settings
from Display import menu
from Saves.save_settings import save_resolution_to_json, load_resolution_from_json, save_keys_to_json

running = True
game_is_on = False
json_width, json_height = load_resolution_from_json()

display_instance = display_settings.Screen(width=json_width,
                                           height=json_height)
screen = display_instance.screen
index = display_instance.index
icon = display_instance.icon
speed = display_instance.speed
fps = display_instance.clock

menu_instance = menu.mainMenu(display_instance, game_is_on)
menu_screen = menu_instance.main_menu
music_instance = menu_instance.main_music
control_menu = menu_instance.create_keys_menu()


def noop():
    pass


update_resolution = noop

if json_height == 900:
    update_resolution = menu_instance.update_menu_position_900
    print(update_resolution)
    print(300)
elif json_height == 768:
    update_resolution = menu_instance.update_menu_position_768
    print(250)

elif json_height == 720:
    update_resolution = menu_instance.update_menu_position_720
    print(200)


def main() -> None:
    global update_resolution
    global running
    global index
    global menu_screen
    global game_is_on

    while running:
        background_image = display_instance.get_frames
        if music_instance.menu_music_is_playing:
            music_instance.check_music()
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                running = False

            if menu_instance.in_keybinding_mode:
                # if event.type == pygame.KEYDOWN:
                key_name = pygame.key.name(event.key)
                print(key_name)
                if key_name == "backspace":
                    menu_instance.in_keybinding_mode = False
                elif key_name and key_name not in menu_instance.default_key_bindings.values():
                    menu_instance.default_key_bindings[menu_instance.current_action] = key_name
                    save_keys_to_json(menu_instance.default_key_bindings)
                    menu_instance.current_label.set_title(f"{menu_instance.current_action}-{key_name}")
                    menu_instance.in_keybinding_mode = False
                else:
                    print("Invalid key or key already bound!")
                    menu_instance.in_keybinding_mode = False

        if pygame.time.get_ticks() % speed == 0:
            index = (index + 1) % len(background_image)

        if display_instance.resolution_changed:
            update_resolution()
            save_resolution_to_json(screen.get_width(), screen.get_height())
            display_instance.resolution_changed = False

        if menu_screen.is_enabled():
            menu_screen.update(events)
            music_volume = menu_instance.settings.get_widget("volume").get_value()
            menu_instance.adjust_music_volume(music_volume)
            screen.blit(background_image[index], (0, 0))
            menu_screen.draw(screen)
            fps.tick(180)
            pygame.display.flip()

        if menu_instance.game_global:
            menu_screen.disable()

        else:
            menu_screen.enable()

    pygame.quit()


if __name__ == "__main__":
    main()
