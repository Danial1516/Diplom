from kivy.properties import StringProperty
from kivymd.uix.screen import MDScreen

class TimeTest(MDScreen):
    selected_time = StringProperty('30 секунд')  # Свойство для хранения выбранного времени

    def set_time_and_navigate(self, time):
        self.selected_time = time  # Устанавливаем выбранное время
        self.manager.current = 'time_test_questions'  # Переход на экран