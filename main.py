# main.py

from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager
from kivymd.app import MDApp
from kivymd.toast import toast
from ui.screens import LoginScreen, RegisterScreen, MainScreen, HomeScreen, TasksScreen, RatingScreen, NotificationsScreen, ChatScreen
from logic.auth import login_user, register_user
from logic.chat import show_greeting, show_translation, show_lexicon, show_grammar, show_phonetics
import logging
from kivymd.uix.pickers import MDDatePicker
from kivy.core.window import Window
from googletrans import Translator
import os

logging.basicConfig(level=logging.DEBUG)
Window.size = (360, 640)  # Устанавливаем размеры окна с соотношением сторон 9:16

class LangVoyageApp(MDApp):
    current_user = None
    translator = Translator()

    def build(self):
        kv_path = os.path.join(os.path.dirname(__file__), 'ui', 'kv')
        Builder.load_file(os.path.join(kv_path, 'login_screen.kv'))
        Builder.load_file(os.path.join(kv_path, 'register_screen.kv'))
        Builder.load_file(os.path.join(kv_path, 'main_screen.kv'))
        Builder.load_file(os.path.join(kv_path, 'home_screen.kv'))
        Builder.load_file(os.path.join(kv_path, 'tasks_screen.kv'))
        Builder.load_file(os.path.join(kv_path, 'rating_screen.kv'))
        Builder.load_file(os.path.join(kv_path, 'notifications_screen.kv'))
        Builder.load_file(os.path.join(kv_path, 'chat_screen.kv'))

        sm = ScreenManager()
        sm.add_widget(LoginScreen(name='login'))
        sm.add_widget(RegisterScreen(name='register'))
        sm.add_widget(MainScreen(name='main'))
        sm.add_widget(HomeScreen(name='home'))
        sm.add_widget(TasksScreen(name='tasks'))
        sm.add_widget(RatingScreen(name='rating'))
        sm.add_widget(NotificationsScreen(name='notifications'))
        sm.add_widget(ChatScreen(name='chat'))
        return sm

    def login(self):
        email = self.root.get_screen('login').ids.login_email.text
        password = self.root.get_screen('login').ids.login_password.text
        if login_user(email, password):
            self.current_user = email
            toast("Login successful!")
            self.root.current = 'main'
        else:
            toast("Invalid email or password")

    def register(self):
        name = self.root.get_screen('register').ids.register_name.text
        email = self.root.get_screen('register').ids.register_email.text
        password = self.root.get_screen('register').ids.register_password.text
        if register_user(name, email, password):
            toast("Registration successful!")
            self.root.current = 'login'
        else:
            toast("Email already exists")
            logging.error(f"Registration failed for email: {email}")

    def show_user(self):
        toast(f"Logged in as {self.current_user}")

    def on_start(self):
        show_greeting(self)

    def show_date_picker(self):
        date_dialog = MDDatePicker()
        date_dialog.open()

if __name__ == '__main__':
    LangVoyageApp().run()
