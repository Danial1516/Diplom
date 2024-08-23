import os
import random
import pygame
from kivymd.uix.screen import MDScreen
from kivy.properties import StringProperty

class ListenScreen(MDScreen):
    current_level = StringProperty('A1')  # Уровень сложности
    current_file_name = StringProperty('')  # Название текущего аудиофайла

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        pygame.mixer.init()
        self.sound_file = None
        self.is_playing = False
        self.current_time = 0

    def set_level(self, level):
        """Установите текущий уровень."""
        if level in ['A1', 'A2', 'B1', 'B2', 'C1']:
            self.current_level = level
            self.sound_file = None
            self.current_file_name = ''
        else:
            print("Invalid level")

    def play_audio(self):
        """Воспроизведение случайного аудиофайла или пауза/возобновление воспроизведения."""
        directory = f'assets/audio/{self.current_level}'
        mp3_files = [f for f in os.listdir(directory) if f.endswith('.mp3')]

        if not mp3_files:
            print("No MP3 files found in the directory.")
            return

        file_name = random.choice(mp3_files)
        self.current_file_name = file_name
        file_path = os.path.join(directory, file_name)

        if self.sound_file:
            if self.is_playing:
                self.current_time = pygame.mixer.music.get_pos() / 1000
                pygame.mixer.music.pause()
                self.is_playing = False
            else:
                pygame.mixer.music.unpause()
                self.is_playing = True
        else:
            pygame.mixer.music.load(file_path)
            pygame.mixer.music.play()
            self.is_playing = True
            self.sound_file = file_path

    def on_pre_enter(self, *args):
        """Сброс состояния при входе на экран."""
        if self.sound_file:
            pygame.mixer.music.stop()
            self.sound_file = None
            self.is_playing = False
            self.current_time = 0

    def on_leave(self, *args):
        """Сброс состояния при выходе с экрана."""
        if self.sound_file:
            pygame.mixer.music.stop()
            self.sound_file = None
            self.is_playing = False
            self.current_time = 0
