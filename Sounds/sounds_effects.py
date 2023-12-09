from pygame_menu import sound
from pygame import mixer
import random
import pygame


class MusicEffects:
    def __init__(self):
        self.engine = sound.Sound()
        self.engine.set_sound(sound.SOUND_TYPE_CLICK_MOUSE, "Sounds/mixkit-interface-click-menu.wav")
        self.engine.set_sound(sound.SOUND_TYPE_WIDGET_SELECTION, "Sounds/mixkit-hard-typewriter-click-menu_opener.wav")


class MainMusic:
    def __init__(self):
        self.music_files = [
            "Sounds/10 - Space Invaders - Odyssey v2.2b.mp3",
            "Sounds/05 - Space Invaders - Future.mp3",
            "Sounds/Space Invaders - Theme.mp3",
            "Sounds/At Dooms Gate.mp3",
        ]
        self.main_ingame_theme = "Sounds/Space Invaders - Syndicate-Game_Music.mp3"
        mixer.init(channels=3)
        self.volume = mixer.music.get_volume()
        print(self.volume)

        self.menu_music_is_playing = True

    def play_next_music(self) -> None:
        next_song = random.choice(self.music_files)
        pygame.mixer.music.load(next_song)
        pygame.mixer.music.play()

    def check_music(self) -> None:
        if not pygame.mixer.music.get_busy() and self.menu_music_is_playing:
            self.play_next_music()

    def stop_music(self) -> None:
        self.menu_music_is_playing = False
        pygame.mixer.music.pause()
        pygame.time.delay(2000)
        self.game_music()

    def continue_music(self) -> None:
        self.menu_music_is_playing = True
        pygame.mixer.music.pause()
        pygame.time.delay(2000)
        self.check_music()

    def set_volume(self, volume) -> None:
        if not pygame.mixer.get_init():
            pygame.mixer.init()
        if pygame.mixer.music.get_busy() and self.menu_music_is_playing:
            self.volume = volume
            pygame.mixer.music.set_volume(self.volume)

    def game_music(self) -> None:
        self.menu_music_is_playing = False
        pygame.mixer_music.load(self.main_ingame_theme)
        pygame.mixer.music.play()


class GameEffects(MainMusic):
    def __init__(self):
        super().__init__()
        self.blaster_channel = mixer.Channel(1)
        self.blaster_sound = mixer.Sound("Sounds/LaserBlastQuick PE1095107.mp3")

        self.blaster_explosionChannel = mixer.Channel(2)
        self.blaster_explosion_sound = mixer.Sound("Sounds/medium-explosion-40472.mp3")

        self.rocket_channel = mixer.Channel(3)
        self.rocket_sound = mixer.Sound("Sounds/SpaceLaserShot PE1095407.mp3")

        self.rocket_explosionChannel = mixer.Channel(4)
        self.rocket_explosion_sound = mixer.Sound("Sounds/low-impactwav-14905.mp3")

    def ship_blasters(self) -> None:
        self.blaster_channel.play(self.blaster_sound)
        self.blaster_channel.set_volume(self.volume)

    def blaster_explosion(self) -> None:
        self.blaster_explosionChannel.play(self.blaster_explosion_sound)
        self.blaster_explosionChannel.set_volume(self.volume)

    def ship_rocket(self) -> None:
        self.rocket_channel.play(self.rocket_sound)
        self.rocket_channel.set_volume(self.volume)

    def rocket_explosion(self) -> None:
        self.rocket_explosionChannel.play(self.rocket_explosion_sound)
        self.rocket_explosionChannel.set_volume(self.volume)
