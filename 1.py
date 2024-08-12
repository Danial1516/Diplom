from kivy.lang import Builder
from kivymd.app import MDApp
from kivy.uix.screenmanager import ScreenManager
from logic.calendar_screen import CalendarScreen

class LangVoyageApp(MDApp):
    def build(self):
        self.theme_cls.theme_style = "Light"
        self.theme_cls.primary_palette = "Blue"
        screen_manager = ScreenManager()
        screen_manager.add_widget(CalendarScreen(name="calendar_screen"))
        return screen_manager

if __name__ == "__main__":
    Builder.load_file("ui/kv/calendar_screen.kv")
    LangVoyageApp().run()
