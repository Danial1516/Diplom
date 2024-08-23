import pygame
from kivymd.uix.screen import MDScreen
import os
import random
from kivy.properties import StringProperty

class ListenScreen(MDScreen):
    current_file_name = StringProperty('')
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        pygame.mixer.init()
        self.current_level = 'A1'  # Установите уровень по умолчанию
        self.sound_file = None  # Путь к файлу
        self.is_playing = False  # Флаг для отслеживания состояния воспроизведения
        self.current_time = 0  # Текущая позиция воспроизведения

    def set_level(self, level):
        """Установите текущий уровень."""
        if level in ['A1', 'A2', 'B1', 'B2', 'C1']:
            self.current_level = level
        else:
            print("Invalid level")

    def play_audio(self):
        """Воспроизведение аудиофайла или пауза/возобновление воспроизведения."""

        directory = f'assets/audio/{self.current_level}'
        mp3_files = os.listdir(directory)
        file_name = random.choice(mp3_files)
        file_path = os.path.join(directory, file_name)

        if self.sound_file:
            if self.is_playing:
                # Пауза текущего воспроизведения и сохранение позиции
                self.current_time = pygame.mixer.music.get_pos() / 1000
                pygame.mixer.music.pause()
                self.is_playing = False
            else:
                # Возобновление воспроизведения с сохраненной позиции
                pygame.mixer.music.unpause()
                self.is_playing = True
        else:
            # Если аудио не было загружено, загрузите и воспроизведите его
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



