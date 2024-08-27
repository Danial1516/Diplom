import random
import os
import pygame
from kivymd.uix.screen import MDScreen
from kivy.properties import StringProperty

class ListenScreen(MDScreen):
    current_file_name = StringProperty('')
    play_icon = StringProperty('play')

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
        if self.current_file_name:
            file_path = os.path.join(f'assets/audio/{self.current_level}', self.current_file_name + '.mp3')

            if self.sound_file:
                if self.is_playing:
                    # Пауза текущего воспроизведения и сохранение позиции
                    self.current_time = pygame.mixer.music.get_pos() / 1000
                    pygame.mixer.music.pause()
                    self.play_icon = 'play'
                    self.is_playing = False
                else:
                    # Возобновление воспроизведения с сохраненной позиции
                    pygame.mixer.music.unpause()
                    self.is_playing = True
                    self.play_icon = 'pause'
            else:
                # Если аудио не было загружено, загрузите и воспроизведите его
                pygame.mixer.music.load(file_path)
                pygame.mixer.music.play()
                self.is_playing = True
                self.sound_file = file_path

    def get_text_file_path(self):
        """Получить путь к текстовому файлу, соответствующему текущему аудиофайлу."""
        return os.path.join('assets/audio/questions', self.current_file_name + '.txt')

    def on_pre_enter(self, *args):
        """Сброс состояния при входе на экран."""
        if self.sound_file:
            pygame.mixer.music.stop()
            self.sound_file = None
            self.is_playing = False
            self.play_icon = 'play'
            self.current_time = 0

        # Установите название текущего файла при входе на экран
        directory = f'assets/audio/{self.current_level}'
        mp3_files = os.listdir(directory)
        if mp3_files:
            file_name = random.choice(mp3_files)
            # Удалите расширение .mp3 из имени файла
            self.current_file_name, _ = os.path.splitext(file_name)

            # Обновите экран с вопросами
            audio_screen = self.manager.get_screen('audio_question')
            audio_screen.update_screen_with_audio(self.current_file_name)

    def on_leave(self, *args):
        """Сброс состояния при выходе с экрана."""
        if self.sound_file:
            pygame.mixer.music.stop()
            self.sound_file = None
            self.is_playing = False
            self.current_time = 0
