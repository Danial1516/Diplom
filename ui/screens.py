# ui/screens.py
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.scrollview import ScrollView
from kivymd.uix.card import MDCard, MDSeparator
from kivymd.uix.screen import MDScreen
from kivymd.uix.label import MDLabel
from datetime import datetime, timedelta
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.pickers import MDDatePicker
from sqlalchemy.exc import SQLAlchemyError

from database.db import SessionLocal, Notification


class LoginScreen(MDScreen):
    pass

class RegisterScreen(MDScreen):
    pass

class MainScreen(MDScreen):
    pass

class HomeScreen(MDScreen):
    pass

class TasksScreen(MDScreen):
    pass

class RatingScreen(MDScreen):
    pass

class CustMDCard(MDCard):
    def __init__(self, **kwargs):
        print("Initializing CustMDCard")
        super(CustMDCard, self).__init__(**kwargs)


class NotificationsScreen(MDScreen):
    def on_kv_post(self, base_widget):
        super(NotificationsScreen, self).on_kv_post(base_widget)
        print("Loading notifications")
        self.load_notifications()

    def load_notifications(self):
        try:
            # Создаем сессию для работы с базой данных
            session = SessionLocal()

            # Получаем все уведомления из базы данных
            notifications = session.query(Notification).all()

            # Получаем ссылку на MDBoxLayout, куда будут добавляться карточки
            notifications_box = self.ids.notifications_box

            # Очищаем все предыдущие карточки
            notifications_box.clear_widgets()

            # Создаем и добавляем карточки для каждого уведомления
            for notification in reversed(notifications):
                card = CustMDCard()
                card.ids.title_label.text = notification.title
                card.ids.description_label.text = notification.description
                notifications_box.add_widget(card, index=0)  # Добавляем карточку в начало

            # Закрываем сессию
            session.close()

        except Exception as e:
            print(f"An error occurred: {e}")


class TimeConstructionsScreen(MDScreen):
    pass

class PresentSimpleScreen(MDScreen):
    pass

class PresentPerfectScreen(MDScreen):
    pass

class PastSimpleScreen(MDScreen):
    pass

class FutureContinuousScreen(MDScreen):
    pass

class FutureSimpleScreen(MDScreen):
    pass

class PastPerfectContinuousScreen(MDScreen):
    pass

class PastPerfectScreen(MDScreen):
    pass

class PastContinuousScreen(MDScreen):
    pass


class FuturePerfectContinuousScreen(MDScreen):
    pass

class FuturePerfectScreen(MDScreen):
    pass

class ExpresPreferencesScreen(MDScreen):
    pass

class SpecialPhrasesWordsScreen(MDScreen):
    pass

class GrammaScreen(MDScreen):
    pass

class PresentPerfectContinuousScreen(MDScreen):
    pass

class PresentContinuousScreen(MDScreen):
    pass

class CalendarScreen(MDScreen):
    pass
