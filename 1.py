from kivy.lang import Builder
from kivy.metrics import dp
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.boxlayout import BoxLayout
from kivymd.app import MDApp
from kivymd.uix.card import MDSeparator
from kivymd.uix.label import MDLabel
from kivy.graphics import Color, Rectangle
from sqlalchemy.orm import sessionmaker
from database.db import User, Rating, SessionLocal

# Kivy язык для описания интерфейса
kv = '''
<RatingScreen>:
    MDBoxLayout:
        orientation: 'vertical'
        md_bg_color: 28/255, 140/255, 140/255, 1

        MDBoxLayout:
            orientation: 'horizontal'
            size_hint_y: None
            height: dp(48)
            spacing: dp(10)
            padding: dp(10)

            MDRaisedButton:
                text: "30 секунд"
                on_release: root.update_ratings('thirty_sec')

            MDRaisedButton:
                text: "1 хвилина"
                on_release: root.update_ratings('one_min')

            MDRaisedButton:
                text: "3 хвилини"
                on_release: root.update_ratings('three_min')

        MDScrollView:
            MDList:
                id: rating_list
                # Вставляем заголовки столбцов
                MDBoxLayout:
                    orientation: 'horizontal'
                    size_hint_y: None
                    height: dp(48)
                    padding: dp(10)

                    MDLabel:
                        text: "№"
                        size_hint_x: 0.1
                        halign: 'center'

                    MDSeparator:
                        orientation: 'vertical'
                        width: dp(1)
                        color: 0, 0, 0, 1

                    MDLabel:
                        text: "Ім'я"
                        size_hint_x: 0.6
                        halign: 'center'

                    MDSeparator:
                        orientation: 'vertical'
                        width: dp(1)
                        color: 0, 0, 0, 1

                    MDLabel:
                        text: "Бали"
                        size_hint_x: 0.3
                        halign: 'center'

                MDSeparator:
                    height: dp(2)
'''


class RatingScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
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


class MyApp(MDApp):
    def build(self):
        Builder.load_string(kv)
        sm = ScreenManager()
        sm.add_widget(RatingScreen(name='rating_screen'))
        return sm


if __name__ == '__main__':
    MyApp().run()
