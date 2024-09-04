from kivy.properties import ObjectProperty
from kivymd.uix.menu import MDDropdownMenu
from kivymd.uix.screen import MDScreen

class TimeTestQuestions(MDScreen):
    def on_pre_enter(self, *args):
        time_test_screen = self.manager.get_screen('time_test')
        selected_time = time_test_screen.selected_time  # Получаем выбранное время
        print(f"Выбранное время: {selected_time}")