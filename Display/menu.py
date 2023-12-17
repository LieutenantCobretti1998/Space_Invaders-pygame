import pygame_menu as pm
from pygame_menu.widgets import Widget
from pygame_menu import Menu
from Display import themes_and_fonts
from Sounds import sounds_effects
from Display import game_display
from Saves.save_settings import (load_keys_from_json, load_volume_from_json, save_volume_to_json, save_keys_to_json,
                                 restore_default_keys, default_settings)


class mainMenu:
    def __init__(self, screen, *args):
        self.default_keys = default_settings
        self.restore_default = None
        self.default_key_bindings = load_keys_from_json()
        self.restore_keys = restore_default_keys
        self.in_keybinding_mode = False
        self.current_action = None
        self.new_key = None
        self.current_label = None
        self.main_theme = themes_and_fonts.menu_transparency_theme
        self.pause_menu_theme = themes_and_fonts.menu_black_background
        self.effects = sounds_effects.MusicEffects()
        self.sound_engine = self.effects.engine
        self.main_music = sounds_effects.MainMusic()
        self.window = screen
        self.screen = self.window.screen
        self.resolution = screen.change_resolution
        self.saved_res = f"{self.window.width} x {self.window.height}"
        self.keys = self.create_keys_menu()
        self.settings = self.settings_menu()
        self.main_menu = self.create_menu(self.window.width / 2, self.window.height / 2)
        self.game_global = args[0]

    def create_menu(self, width, height) -> Menu:
        menu = pm.Menu("Space Invaders", width, height, theme=self.main_theme)
        menu.add.button("Start Game", self.start_game, button_id="start")
        menu.add.button("Settings", self.settings, button_id="settings")
        menu.add.button("Quit game", pm.events.EXIT)
        menu.set_sound(self.sound_engine, recursive=True)
        return menu

    def create_pause_menu(self, width, height) -> Menu:
        pause_menu = pm.Menu("Game is paused", width, height, theme=self.pause_menu_theme)
        pause_menu.add.label("Press space to return to main menu")
        pause_menu.add.label("Press backspace to resume game")
        pause_menu.set_sound(self.sound_engine, recursive=True)
        return pause_menu

    def settings_menu(self) -> Menu:
        resolutions = [
            ("1280 x 720", "1280 x 720"),
            ("1366 x 768", "1366 x 768"),
            ("1600 x 900", "1600 x 900")
        ]
        settings = pm.Menu("Settings", self.window.width / 2, self.window.height / 2, theme=self.main_theme)
        settings.add.button("Control", self.keys, button_id="difficulty", )
        resolution_selector = settings.add.selector("Resolution", resolutions,
                                                    selector_id="resolution",
                                                    onchange=self.resolution,
                                                    )

        def current_res(resolution: str) -> None:
            if any(res for res, _ in resolutions if res == resolution):
                print("yes")
                resolution_selector.set_value(resolution)

        current_res(self.saved_res)

        def format_music_volume(value) -> str:
            return str(round(value))

        default_volume = load_volume_from_json()

        music_volume = settings.add.range_slider("Toggle music", default_volume, [0, 100],
                                                 increment=1, rangeslider_id="volume", range_text_value_enabled=False,
                                                 value_format=format_music_volume)
        music_level = music_volume.get_value()
        music_volume.set_onchange(self.adjust_music_volume(music_level))

        settings.add.button("Return", pm.events.BACK)
        settings.set_sound(self.sound_engine, recursive=True)
        return settings

    def create_keys_menu(self) -> Menu:
        keys = pm.Menu("Key Bindings", self.window.width / 2, self.window.height / 2, theme=self.main_theme)
        keys.get_height()
        keys.get_width()
        action_list = list(self.default_key_bindings.keys())

        # Left
        label_widget_left = keys.add.label(f"{action_list[0]}-{self.default_key_bindings['left']}",
                                           align=pm.locals.ALIGN_LEFT)
        label_input_left = keys.add.text_input(title="",
                                               maxchar=1,
                                               textinput_id="left")
        label_input_left.set_onchange(lambda x: self.clear_binding(action_list[0],
                                                                   label_widget_left))

        # Right
        label_widget_right = keys.add.label(f"{action_list[1]}-{self.default_key_bindings['right']}",
                                            align=pm.locals.ALIGN_LEFT)
        label_input_right = keys.add.text_input(title="",
                                                maxchar=1,
                                                textinput_id="right")
        label_input_right.set_onchange(lambda x: self.clear_binding(action_list[1],
                                                                    label_widget_right))

        # Up
        label_widget_up = keys.add.label(f"{action_list[2]}-{self.default_key_bindings['up']}",
                                         align=pm.locals.ALIGN_LEFT)
        label_input_up = keys.add.text_input(title="",
                                             maxchar=1,
                                             textinput_id="up")
        label_input_up.set_onchange(lambda x: self.clear_binding(action_list[2],
                                                                 label_widget_up))

        # Down
        label_widget_down = keys.add.label(f"{action_list[3]}-{self.default_key_bindings['down']}",
                                           align=pm.locals.ALIGN_LEFT)
        label_input_down = keys.add.text_input(title="",
                                               maxchar=1,
                                               textinput_id="down")
        label_input_down.set_onchange(lambda x: self.clear_binding(action_list[3],
                                                                   label_widget_down))

        # return button
        self.restore_default = keys.add.button(
            "Restore default settings",
            lambda: self.restore_default_keys(
                label_widget_left, label_input_left, label_widget_right, label_input_right, label_widget_up,
                label_input_up, label_widget_down, label_input_down
            )
        )
        keys.add.button("Back", pm.events.BACK)
        return keys

    def restore_default_keys(self, *args) -> None:
        save_keys_to_json(self.default_keys)
        self.default_key_bindings = load_keys_from_json()

        args[0].set_title(f"left-{self.default_key_bindings['left']}")
        args[1].set_value("")
        args[2].set_title(f"right-{self.default_key_bindings['right']}")
        args[3].set_value("")
        args[4].set_title(f"up-{self.default_key_bindings['up']}")
        args[5].set_value("")
        args[6].set_title(f"down-{self.default_key_bindings['down']}")
        args[7].set_value("")

    def clear_binding(self, action: str, label: Widget) -> None:
        if self.is_key_dublicate(action):
            return
        self.in_keybinding_mode = True
        self.current_action = action
        print(self.current_action)
        self.current_label = label

    def is_key_dublicate(self, new_key: str) -> bool:
        # for action, key in self.default_key_bindings.items():
        #     if action != current_action and key == new_key:
        #         return True
        #     return False
        if new_key in self.default_key_bindings.values():
            return True
        return False

    def update_menu_position_720(self) -> Menu:
        menu_x = 0
        menu_y = 0

        if self.window.width == 1280:
            menu_x = 50
            menu_y = 50

        if self.window.width == 1366:
            menu_x = 55
            menu_y = 55

        if self.window.width == 1600:
            menu_x = 70
            menu_y = 70

        print(200)
        print(menu_x, menu_y)
        self.settings.set_relative_position(menu_x, menu_y)
        self.keys.set_relative_position(menu_x, menu_y)
        return self.main_menu.set_relative_position(menu_x, menu_y)

    def update_menu_position_768(self) -> Menu:
        menu_x = 0
        menu_y = 0

        if self.window.width == 1280:
            menu_x = 45
            menu_y = 45

        if self.window.width == 1366:
            menu_x = 50
            menu_y = 50

        if self.window.width == 1600:
            menu_x = 65
            menu_y = 65

        print(200)
        print(menu_x, menu_y)
        self.settings.set_relative_position(menu_x, menu_y)
        self.keys.set_relative_position(menu_x, menu_y)
        return self.main_menu.set_relative_position(menu_x, menu_y)

    def update_menu_position_900(self) -> Menu:
        menu_x = 0
        menu_y = 0

        if self.window.width == 1280:
            menu_x = 30
            menu_y = 30

        if self.window.width == 1366:
            menu_x = 35
            menu_y = 35

        if self.window.width == 1600:
            menu_x = 50
            menu_y = 50

        print(200)
        print(menu_x, menu_y)
        self.settings.set_relative_position(menu_x, menu_y)
        self.keys.set_relative_position(menu_x, menu_y)
        return self.main_menu.set_relative_position(menu_x, menu_y)

    def adjust_music_volume(self, value) -> None:
        volume = round(value) / 100
        self.main_music.set_volume(volume)
        save_volume_to_json(value)

    def start_game(self) -> bool:
        self.main_music.stop_music()
        self.main_music.game_music()
        game_instance = game_display.Game(self.window.width, self.window.height, self.create_pause_menu,
                                          self.main_menu.draw(self.screen), self.main_music.continue_music,
                                          self.game_global, self.default_key_bindings)
        self.game_global = True
        game_instance.game_screen()
        self.game_global = game_instance.game_global
        return self.game_global
