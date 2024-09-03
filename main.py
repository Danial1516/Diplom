# main.py
from database.db import create_tables
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, NoTransition
from kivymd.app import MDApp
from kivymd.toast import toast
from ui.screens import LoginScreen, RegisterScreen, SpecialPhrasesWordsScreen, ExpresPreferencesScreen, FuturePerfectScreen, GrammaScreen, FuturePerfectContinuousScreen,PastSimpleScreen,PastContinuousScreen, FutureContinuousScreen, FutureSimpleScreen, PastPerfectScreen, PastPerfectContinuousScreen, MainScreen,PresentPerfectScreen,PresentPerfectContinuousScreen, HomeScreen, TasksScreen, RatingScreen, NotificationsScreen, TimeConstructionsScreen, PresentSimpleScreen, PresentContinuousScreen
from logic.auth import login_user, register_user
from logic.chat import ChatScreen
from logic.learn import ElevatedWidget
from logic.task import SpecCard
from logic.time_test import TimeTest
from logic.time_test_questions import TimeTestQuestions
from logic.testing import TestingScreen
from logic.testing_questions import TestingQuestions
from logic.audio_quest import AudioQuestionsScreen
from logic.listening import ListenScreen
from logic.сhoose_lvl_listen import ChooseLvlListenScreen
import logging
from kivymd.uix.pickers import MDDatePicker
from kivy.core.window import Window
from googletrans import Translator
from kivy.core.text import LabelBase
import os

logging.basicConfig(level=logging.DEBUG)
Window.size = (360, 640)  # Устанавливаем размеры окна с соотношением сторон 9:16

class LangVoyageApp(MDApp):
    current_user = None
    translator = Translator()
    def build(self):
        try:
            kv_path = os.path.join(os.path.dirname(__file__), 'ui', 'kv')
            Builder.load_file(os.path.join(kv_path, 'login_screen.kv'))
            Builder.load_file(os.path.join(kv_path, 'register_screen.kv'))
            Builder.load_file(os.path.join(kv_path, 'main_screen.kv'))
            Builder.load_file(os.path.join(kv_path, 'home_screen.kv'))
            Builder.load_file(os.path.join(kv_path, 'tasks_screen.kv'))
            Builder.load_file(os.path.join(kv_path, 'rating_screen.kv'))
            Builder.load_file(os.path.join(kv_path, 'notifications_screen.kv'))
            Builder.load_file(os.path.join(kv_path, 'chat_screen.kv'))
            Builder.load_file(os.path.join(kv_path, 'time_constr.kv'))
            Builder.load_file(os.path.join(kv_path, 'present_simple_screen.kv'))
            Builder.load_file(os.path.join(kv_path, 'present_continuous_screen.kv'))
            Builder.load_file(os.path.join(kv_path, 'present_perfect_screen.kv'))
            Builder.load_file(os.path.join(kv_path, 'present_perfect_continuous_screen.kv'))
            Builder.load_file(os.path.join(kv_path, 'past_simple.kv'))
            Builder.load_file(os.path.join(kv_path, 'future_continuous_screen.kv'))
            Builder.load_file(os.path.join(kv_path, 'future_simple_screen.kv'))
            Builder.load_file(os.path.join(kv_path, 'past_continuous_screen.kv'))
            Builder.load_file(os.path.join(kv_path, 'past_perfect_continuous.kv'))
            Builder.load_file(os.path.join(kv_path, 'past_perfect_screen.kv'))
            Builder.load_file(os.path.join(kv_path, 'future_perfect_continuous_screen.kv'))
            Builder.load_file(os.path.join(kv_path, 'future_perfect_screen.kv'))
            Builder.load_file(os.path.join(kv_path, 'gramm_screen.kv'))
            Builder.load_file(os.path.join(kv_path, 'expression_of_preferences.kv'))
            Builder.load_file(os.path.join(kv_path, 'spec_phrases_words.kv'))
            Builder.load_file(os.path.join(kv_path, 'listening.kv'))
            Builder.load_file(os.path.join(kv_path, 'chose_lvl_list.kv'))
            Builder.load_file(os.path.join(kv_path, 'audio_questions.kv'))
            Builder.load_file(os.path.join(kv_path, 'testing.kv'))
            Builder.load_file(os.path.join(kv_path, 'testing_questions.kv'))
            Builder.load_file(os.path.join(kv_path, 'time_test.kv'))
            Builder.load_file(os.path.join(kv_path, 'time_test_questions.kv'))

            sm = ScreenManager(transition=NoTransition())
            sm.add_widget(LoginScreen(name='login'))
            sm.add_widget(RegisterScreen(name='register'))
            sm.add_widget(MainScreen(name='main'))
            sm.add_widget(HomeScreen(name='home'))
            sm.add_widget(TasksScreen(name='tasks'))
            sm.add_widget(RatingScreen(name='rating'))
            sm.add_widget(NotificationsScreen(name='notifications'))
            sm.add_widget(ChatScreen(name='chat'))
            sm.add_widget(TimeConstructionsScreen(name='time_c'))
            sm.add_widget(PresentSimpleScreen(name='present_simple'))
            sm.add_widget(PresentContinuousScreen(name='present_continuous'))
            sm.add_widget((PresentPerfectScreen(name="present_perfect")))
            sm.add_widget((PresentPerfectContinuousScreen(name="present_perfect_continuous")))
            sm.add_widget((PastSimpleScreen(name="past_simple")))
            sm.add_widget((FutureContinuousScreen(name="future_continuous")))
            sm.add_widget((FutureSimpleScreen(name="future_simple")))
            sm.add_widget((PastPerfectContinuousScreen(name="past_perfect_continuous")))
            sm.add_widget((PastPerfectScreen(name="past_perfect")))
            sm.add_widget((PastContinuousScreen(name="past_continuous")))
            sm.add_widget((FuturePerfectScreen(name="future_perfect")))
            sm.add_widget((FuturePerfectContinuousScreen(name="future_perfect_continuous")))
            sm.add_widget((GrammaScreen(name="gramm_struct")))
            sm.add_widget((ExpresPreferencesScreen(name="expres_preferences")))
            sm.add_widget((SpecialPhrasesWordsScreen(name="spec_phrases_words")))
            sm.add_widget((ListenScreen(name="listen_screen")))
            sm.add_widget((ChooseLvlListenScreen(name="choose_lvl_listen")))
            sm.add_widget((AudioQuestionsScreen(name="audio_question")))
            sm.add_widget((TestingScreen(name="testing")))
            sm.add_widget((TestingQuestions(name="testing_questions")))
            sm.add_widget((TimeTest(name="time_test")))
            sm.add_widget((TimeTestQuestions(name="time_test_questions")))


            logging.info("Все экраны загружены успешно.")
            return sm

        except Exception as e:
            logging.error(f"Ошибка при загрузке экранов: {e}")
            return None

    def change_screen_item(self, screen_name):
        self.root.current = screen_name

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

    def show_date_picker(self):
        date_dialog = MDDatePicker()
        date_dialog.open()



if __name__ == '__main__':
    LabelBase.register(name="Poppins", fn_regular="assets/fonts/beer_money.ttf")
    LabelBase.register(name="BPoppins", fn_regular="assets/fonts/Christmas_ScriptC.ttf")
    LabelBase.register(name="Boom", fn_regular="assets/fonts/Boomboom.otf")
    LabelBase.register(name="Clearsan", fn_regular="assets/fonts/ClearSans-Medium.ttf")  # defolt text
    LabelBase.register(name="Foglih", fn_regular="assets/fonts/FoglihtenNo06_076.otf")
    LabelBase.register(name="Intro", fn_regular="assets/fonts/Intro.otf")
    LabelBase.register(name="juneg", fn_regular="assets/fonts/junegull rg.otf")  # заголовки
    create_tables()
    LangVoyageApp().run()
