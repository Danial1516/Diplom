# ui/screens.py
from kivy.metrics import dp
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.scrollview import ScrollView
from kivymd.uix.card import MDCard, MDSeparator
from kivymd.uix.screen import MDScreen
from kivymd.uix.label import MDLabel
from datetime import datetime, timedelta
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.pickers import MDDatePicker
from sqlalchemy.exc import SQLAlchemyError

from database.db import SessionLocal, Notification, User, Rating


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
    def on_kv_post(self, base_widget):
        super().on_kv_post(base_widget)
        self.session = SessionLocal()  # Используем SessionLocal, который импортирован из database.db
        self.update_ratings('thirty_sec')  # По умолчанию показываем рейтинг для 30 секунд

    def update_ratings(self, category):
        rating_list = self.ids.rating_list
        rating_list.clear_widgets()

        # Вставляем заголовки столбцов
        header = BoxLayout(
            orientation='horizontal',
            size_hint_y=None,
            height=dp(48),
            padding=dp(10)
        )
        header.add_widget(
            MDLabel(
                text="№",
                size_hint_x=0.1,
                halign='center'
            )
        )
        header.add_widget(
            MDSeparator(
                orientation='vertical',
                width=dp(1),
                color=(0, 0, 0, 1)
            )
        )
        header.add_widget(
            MDLabel(
                text="Ім'я",
                size_hint_x=0.6,
                halign='center'
            )
        )
        header.add_widget(
            MDSeparator(
                orientation='vertical',
                width=dp(1),
                color=(0, 0, 0, 1)
            )
        )
        header.add_widget(
            MDLabel(
                text="Бали",
                size_hint_x=0.3,
                halign='center'
            )
        )
        rating_list.add_widget(header)

        # Добавляем разделитель под заголовками
        rating_list.add_widget(MDSeparator(height=dp(2)))

        # Получаем рейтинги по выбранной категории
        ratings = self.session.query(User, Rating).join(Rating).order_by(getattr(Rating, category).desc()).all()

        for i, (user, rating) in enumerate(ratings, start=1):
            item_layout = BoxLayout(
                orientation='horizontal',
                size_hint_y=None,
                height=dp(48),
                padding=dp(10)
            )
            item_layout.add_widget(
                MDLabel(
                    text=f"{i}.",
                    size_hint_x=0.1,
                    halign='center'
                )
            )
            item_layout.add_widget(
                MDSeparator(
                    orientation='vertical',
                    width=dp(1),
                    color=(0, 0, 0, 1)
                )
            )
            item_layout.add_widget(
                MDLabel(
                    text=user.name,
                    size_hint_x=0.6,
                    halign='center'
                )
            )
            item_layout.add_widget(
                MDSeparator(
                    orientation='vertical',
                    width=dp(1),
                    color=(0, 0, 0, 1)
                )
            )
            item_layout.add_widget(
                MDLabel(
                    text=f"{getattr(rating, category)}",
                    size_hint_x=0.3,
                    halign='center'
                )
            )
            rating_list.add_widget(item_layout)

            # Добавляем разделитель под каждой строкой
            rating_list.add_widget(MDSeparator(height=dp(2)))

class CustMDCard(MDCard):
    def __init__(self, **kwargs):
        super(CustMDCard, self).__init__(**kwargs)


class NotificationsScreen(MDScreen):
    def on_kv_post(self, base_widget):
        super(NotificationsScreen, self).on_kv_post(base_widget)
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
